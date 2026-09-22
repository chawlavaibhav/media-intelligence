# Agent 11 — Adversarial Simplicity + Economics/Operations Council

Read-only audit of MI `main` @ `3bb9a3c` (verified `git rev-parse HEAD`), branches `work/pilot-upwork-intro-video-v4` @ `f6ca66f`, `work/upwork-portfolio-samples-2026-09-15` @ `b4b77fa`, Cumin evidence commit `de1f978`, PR #103 head `1de2b37`; UP repo @ `ff06dab`. Prior reviews: `media-intelligence-os-review.md` and `media-intelligence-project-head-review.md` (28 Aug, `a89af60`). Every count below was computed by the command shown or cited; prose figures in PROJECT-MEMORY / CONTROL-STATE were used only after cross-checking the underlying artefact. Labels: OBSERVED / INFERENCE / HYPOTHESIS / UNKNOWN.

Nothing was modified. No provider was called.

---

## 0. Headline numbers (all computed)

| Quantity | Value | Command / source |
|---|---|---|
| Commits on `main`, 24 Aug–15 Sep (23 days) | **899** (≈39/day) | `git rev-list --count HEAD` |
| Merged PRs | 92 | `git log --merges` |
| Tracked files / markdown files / markdown words | 5,288 / 799 / **1,109,283** | `git ls-files`, `wc -w` |
| Governance+coordination+history+shared+PM prose | **207,208 words** | `cat coordination/*.md coordination/decisions/*.md coordination/audits/*.md governance/**.md history/*.md shared/*.md PROJECT-MEMORY.md \| wc -w` |
| Creative guidance that reaches an operator (2 compiled packs + SKILL + WORKFLOW + QA-CHECKLIST + CANON-SHAPE) | **16,023 words** (packs alone 8,854) | same method |
| Ratio governance prose : operator creative guidance | **12.9 : 1** | derived |
| Controller decision records | **117** (64 written 26–28 Aug) | `ls coordination/decisions/` |
| Governance reviews / audits | 8 (205 KB) / 10 docs (28,204 words) | `wc -c governance/reviews/*` |
| Commits whose subject matches governance/controller/audit keywords | **389 / 899 (43%)** | awk over `git log --format=%s` |
| Commits whose subject matches refresh/align/sync/reconcile/snapshot | 98 | same |
| Lines inserted into PROJECT-MEMORY + CONTROL-STATE + WORKSTREAM-STATUS + history/ over their lifetime | **11,317 (+) / 6,122 (−)** | `git log --shortstat -- <paths>` |
| PROJECT-MEMORY.md bytes: 28 Aug (`a89af60`) → post-migration (`baf1c90`, 28 Aug) → HEAD | **105,299 → 18,646 → 38,440** | `git show <sha>:PROJECT-MEMORY.md \| wc -c` |
| CONTROL-STATE.md bytes: `a89af60` → `d164f49` (28 Aug) → HEAD | **21,668 → 12,897 → 30,148** | same |
| Repository bytes by top dir | eval **2.31 GB**; resources 51 MB; canon 30 MB; runtime 1.75 MB; coordination 1.3 MB | `git ls-files -z \| xargs -0 stat -f '%z %N'` |
| Python files / test files / runtime py / runtime tests | 410 / 131 / 97 / 34 | `git ls-files '*.py'` |
| Programme provider spend, Lab (EMP-001 2.664 + EVAL-037 3.229 + EVAL-038 2.260–3.961 + EVAL-040…043 122.241) | **USD 130.4–132.1** | CONTROL-STATE §6 + ledgers (see §2) |
| Programme provider spend, production (cases 001+002+003) | **USD 25.14** (15.393 + 4.660 + 5.091) | TIME-AND-COST.yaml ×3 |
| Production share of provider spend | **≈ 16%** | derived |
| Upwork revenue to date | **USD 0** (0 proposals sent, 0 hires as of 15 Sep) | `UP/LOG.md:803,827`; `UP/ACCOUNTABILITY.md` |

---

## 1. CpAO and TTAO per case (Q1)

### 1.1 Case 001 — UPWORK-INTRO-001 (57-s Upwork profile film, ACCEPTED V4.1)
Source: `production-learning/cases/UPWORK-INTRO-001/TIME-AND-COST.yaml @ 3bb9a3c`, `REVISION-TRACE.yaml`, `HUMAN-VERDICTS.yaml`.

| Metric | Value | Label |
|---|---|---|
| Provider spend, all 54 reserved dispatches | **USD 15.393** (INR ≈ 1,469) | OBSERVED (three ledgers; vendor bill unreconciled) |
| Spend by lineage | V1 3.762 · V2 4.320 · V3 3.284 · V4 4.028 · V4.1 0 | OBSERVED |
| Money in a discarded lineage (V1/V2 contribute no media to V4.1) | **8.082 (52.5%)** | OBSERVED |
| Explicit rejections inside V3/V4 (FLUX 0.03, Kling 0.448, NB2 0.067, Omni 1.014) | 1.559 (10.1%) | OBSERVED |
| Provider failures reserved (Lyria ×3, Veo UNAVAILABLE ×2) | 2.10 (13.6%) | OBSERVED (billing unknown) |
| First-pass generation that reached the accepted asset (residual) | ≈ 3.65 (23.7%) | INFERENCE (15.39 − 8.08 − 1.56 − 2.10) |
| LLM/operator reasoning cost | **not recorded** ("subscription-metered sessions; no per-job figure") | UNKNOWN |
| TTAO (session 1 created → V4.1 film), mechanical lower bound | **7 h 53 m 35 s**; Controller estimate 7–8 h | OBSERVED |
| Generation wait (latency sum / wall windows) | 1 h 05 m 42 s (14%) / up to 24% | OBSERVED |
| Unattributed human review + packaging gaps | **3 h 49 m 34 s (48% of TTAO)** | OBSERVED |
| Executor-agent wall clock | ≈ 4 h 04 m | OBSERVED (derived in file) |
| Versions / human review cycles | 5 / 5 | OBSERVED |
| Human-listed feedback items across the 5 verdicts | 8 + 5 + 7 + 5 = **25** | computed from HUMAN-VERDICTS |
| Media-model failures that reached the Controller | **0** (`SYSTEM-DEFECTS.yaml:114`) | OBSERVED |

**Cost split (money):** generation-that-shipped ≈ 24% · re-generation/discard ≈ 63% (8.08 + 1.56) · provider failure ≈ 14%. **Cost split (time):** waiting on providers 14–24% · human review/packaging gaps 48% · agent execution ≈ 38%. Process, not generation, dominated both.

**Against the Upwork price.** The deliverable (a 57-s presenter film) is the "quoted per project" class: proposed floor **USD 300** for a 30–60 s film / **USD 150** presenter (`UP/PROFILE.md:14, :281-284`; PROPOSED, not live). Promise for that class: 2–4 working days, never express — the 7.9 h wall clock is inside it. Margin at USD 300: provider 5%; the Controller's own review gaps (≥ 3 h 50 m) at the profile's USD 35/h = USD 134; the executor's ≈ 4 h unpriced. If the executor hours were a person at USD 35/h the job nets ≈ USD 9 (3%). PROFILE's own cost model for this class ("$3.76 plus parts; about $250-290 with a day of judgement", `UP/PROFILE.md:284`) already concedes near-zero margin at USD 300.

### 1.2 Case 002 — UPWORK-PORTFOLIO-002 (portfolio tile batch; 9 accepted, 1 skipped)
Source: `production-learning/cases/UPWORK-PORTFOLIO-002/TIME-AND-COST.yaml`, `HUMAN-VERDICTS.yaml`, `REVISION-TRACE.yaml`, `SYSTEM-DEFECTS.yaml @ 3bb9a3c`.

| Metric | Value | Label |
|---|---|---|
| Provider spend (8 paid calls, all returned media) | **USD 4.660** | OBSERVED |
| By version | B1 0 · B2 1.134 (two new static tiles) · N1 1.500 · N2 2.026 · B3 0 | OBSERVED |
| Spent on rejected/skipped (Nivaas story tile N1+N2) | **3.526 (75.7%)** | OBSERVED |
| Accepted tiles that were USD-0 re-exports of prior accepted plates | 7 of 9 | OBSERVED (`portfolio-export/README.md` @ b4b77fa: "nothing generated fresh for the tiles") |
| Per-tile CpAO | 4.660/9 = 0.518 loaded; new static tile direct cost ≈ 0.567 (IronLeaf 0.053 + GyaanBox plate 0.067 + motion 1.014) | OBSERVED |
| Time to outcome (export folder birth → final README), lower bound | **1 h 07 m 33 s** for the set | OBSERVED |
| Generation wait | 12 m 51 s (≈19%) | OBSERVED |
| Human review cycles / human-flagged defects / operator-caught | 5 / **13** / 2 | OBSERVED |
| Model vs pipeline failures reaching the Controller | 2 vs **10** (`SYSTEM-DEFECTS.yaml:188-189`) | OBSERVED |
| Process conformance | NON-CONFORMANT (PD-01…PD-09: bypassed the workflow merged the same morning) | OBSERVED |

**Cost split:** generation that shipped ≈ 24% (1.134) · re-generation/rejected ≈ 76% · process time: of 67 min, ~19% provider wait, the rest human review rounds and compositor repairs. **Against the Upwork price:** the two new tiles are exactly "Static Starter USD 60 (1 concept × 4 sizes)" and GyaanBox additionally a "Video Starter USD 75" text-in-motion clip (`UP/PROFILE.md:215, :226`). Provider cost ≈ 1% of price. The Nivaas story tile is the USD 75 "three-shot product story clip" — failed twice at USD 3.53 (4.7% of price) and was skipped. The batch landed inside the 4-h express window, **but 10 known-class defects reached the customer in the first export** — on a paid order both included revision rounds would have been consumed before the customer saw a clean file.

### 1.3 Case 003 — CUMINCO-CHOPSTICKS-003 (18–25 s spec film, REJECTED ×3)
Source: `de1f978:agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/{JOB.yaml,LEARNING-PACKET.yaml,gen/LEDGER.jsonl,gen/ATTEMPTS.jsonl}`; `1de2b37:production-learning/cases/CUMINCO-CHOPSTICKS-003/*`. Recomputed from the ledgers (python over the two jsonl files):

| Metric | Value | Label |
|---|---|---|
| Ledger lines / attempt records | 101 / 51 (47 ok; 1 local_fault unsent; 1 alias; 1 http_401 quota; 1 refusal) | OBSERVED (computed) |
| Provider spend, all reserved | **USD 5.0907** of a USD 8 cap | OBSERVED (computed = file) |
| By route | veo-3.1-fast-i2v 7 calls 4.200 · nano-banana-2 8 calls 0.536 · gemini-tts 18 calls 0.173 · elevenlabs 8 calls 0.099 · lyria 0.060 · sarvam 8 calls 0.023 | OBSERVED |
| Repair attempts (`is_repair: true`) | 3 attempts, **1.267 (24.9%)** | computed |
| Rejected media | 1.334 (26.2%) | OBSERVED (TIME-AND-COST) |
| Voice search (5 rounds, 26 takes, 4 rounds rejected by ear) | 0.295 (5.8%) | OBSERVED |
| Failed/unsent | 0.0925 (1.8%) | computed |
| Latency sum | 824 s ≈ 13.7 min | computed |
| Working span (planning + 3 versions) / elapsed to final REJECT | ≈ 3 h / **14 h 27 m** (overnight gap) | OBSERVED |
| Human review cycles / versions | **10** / 3 (all rejected) | OBSERVED |
| Model vs pipeline failures reaching the human | 1 vs **5** (`SYSTEM-DEFECTS.yaml:3-5` @ 1de2b37) | OBSERVED |
| CpAO | **undefined (∞)** — no accepted outcome | OBSERVED |
| Process conformance | CONFORMANT ("every gate that existed passed on every version; the user rejected on what no gate measured", case README @ 1de2b37) | OBSERVED |
| Job bookkeeping mass | JOB.yaml + LEARNING-PACKET.yaml = **10,000 words**; case = 4,056 words; 1,403 files on the job branch | computed |

**Cost split:** first-pass generation 73% · repair 25% · failed 2% — but 100% produced nothing accepted. **Against the Upwork price:** an 18–25 s VO'd product story sits between "Video Starter USD 75" and the proposed "30 s piece USD 250". Provider cost would have been 2–7% of price; the human spent 10 review cycles and the job still failed, so the relevant number is not CpAO but **owner minutes per rejected job**.

### 1.4 Cross-case
| | 001 | 002 | 003 |
|---|---|---|---|
| Provider USD | 15.39 | 4.66 | 5.09 |
| Share on discarded/rejected/failed | 63–77% | 76% | 26–52% |
| Human decision points (see §5) | 13 | 11 | 15 |
| Defects found by the human | 25 | 13 | 8 |
| Defects found by a gate before the human | 0 | 2 (operator eye) | 1 (DF-01) |
| Model failures / failures reaching human | 0/25 | 2/13 | 1/8 |
| Accepted | yes (v5) | 9/10 | no |

**OBSERVED:** across three cases, **3 of 46 defects that reached the human (6.5%) were media-model failures; 43 (93.5%) were pipeline, compositor, orchestration or creative-direction failures.** The models are not the bottleneck; the system around them is — and the human was the QA instrument for ≈ 94% of found defects.

---

## 2. Process mass vs outcome (Q17, Q18)

### 2.1 Spend: Lab vs production
| Bucket | USD | Source | Label |
|---|---|---|---|
| EMP-001 (Aug) | 2.664 | CONTROL-STATE §6 | OBSERVED |
| EVAL-037 (reasoning, Sonnet/Haiku) | 3.229 | sum of `calculated_cost_usd` in `eval/experiments/EVAL-037/runs/*/attempt-ledger.json` — **absent from CONTROL-STATE §6** | OBSERVED / conflict |
| EVAL-038 | 2.260 (CONTROL-STATE) vs **3.961** reserve-line sum in `eval/experiments/EVAL-038/runs/spend-ledger.jsonl` | conflict; ambiguous settlements | UNKNOWN which is billed |
| EVAL-040…043 Capability Lab, 8–10 Sep | **122.241** counted against caps; 108.971 produced a sealed artefact; 10.115 produced nothing; vendor bill **never read** | `coordination/audits/AUDIT-2026-09-10-SPEND-RECONCILIATION.md:20-24, :169-172` | OBSERVED |
| **Lab total** | **≈ 130.4–132.1** | | |
| Production (001+002+003) | **25.14** | | OBSERVED |
| Predecessor Media Factory (for context) | ledger USD 35.28 vs dashboard ≈ 34.6 | `MFH/COST-SUMMARY.md` | OBSERVED |

**≈ 84% of provider money went to the Lab; 16% to production.** The 28-Aug project-head review recommended a need-driven admission screen of "~40–60 generations, ~USD 30–40"; the Lab ran 35 Stage-A cases, 311 sealed media, USD 122 (3–4× the recommendation), and then two audits (28k words) to reconcile it — still ending with "the project has an upper bound on its own costs, not a cost".

### 2.2 Words and documents
- Governance/coordination prose **207,208 words** vs operator-facing creative guidance **16,023 words** (12.9:1). Raw accepted Canon corpus (`canon/knowledge/current`, 37 sources) is 44,017 words, of which **2 of 10 packs are compiled** (`ls canon/compilation/`); in Cumin, 10 packs were selected by the trigger table and **2 injected, 8 "missing_domains"** (`JOB.yaml:112-118` @ de1f978).
- `canon/findings` + `candidates` + `experiments` + `research` = 260,784 words of Canon-stream working prose that no operator reads.

### 2.3 Documents before the first creative decision
**RUNBOOK worker chain** (`coordination/RUNBOOK.md:52-63`): PM 38.4 KB + CONTROL-STATE 30.1 KB + PROJECT-CONTRACT 6.0 + COMMUNICATION-STANDARD 5.6 + CONTEXT-SUFFICIENCY 7.7 + charter 3–5.6 + task ≈ **91–99 KB, 7 documents**. The OS review's success test was "≤ 30 KB, stable across three rounds" — **not met**, and PM+CS regrew from 31.5 KB (28 Aug post-migration) to 68.6 KB (+118%) in 18 days.

**Media-agency operator chain** (`.claude/skills/media-agency/BOOTSTRAP.md §2` + SKILL/WORKFLOW/QA/JOB-TEMPLATE): PM (4 sections) · CONTROL-STATE (5 sections) · CANON-SHAPE §4–5 (9.5 KB) · pack-triggers (9.8 KB) · two packs (87.5 KB) · a 61-cell routing table (script output) · ALPHA-1 (10.7 KB) · production-learning README + 2–3 case READMEs + PROMOTION-QUEUEs + ACCEPTED-TEMPLATE + ROUTE-OBSERVATIONS (≈ 40 KB) · UP PROFILE (5 sections of 98.9 KB) · UP LOG last entry · the 5 skill files (69.8 KB). **≈ 24 documents, ≈ 280–330 KB (INFERENCE on the sectioned reads; ~75–85k tokens) before the job's brief is read**, then a 5,298-token Canon prefix per job (`JOB.yaml:117`). Case 001 additionally front-loaded **112 KB of analyst docs** (COMMERCIAL-BRIEF 44.9 KB, CANON-BRIEF 22.7 KB, ROUTE-ANALYSIS 45.1 KB) before the concept memo.

### 2.4 Which components demonstrably reduced CpAO/TTAO (cite) — and which only added sophistication
**Reduced (evidence exists):**
1. **Code-set exact text on textless plates** (compositor + HarfBuzz): V4.1 repair cost **USD 0** (`REVISION-TRACE.yaml:122`), 0 off-deck strings (001 D3), seven strings byte-equal (003 C6). No exact-text defect appears in any HUMAN-VERDICTS across three cases. OBSERVED.
2. **Sealed-media reuse at USD 0**: three EVAL-040 clips + Lyria bed reused in the intro film (`PRODUCTION-MAP-AND-LEARNING.md` rows "sealed … 0"), seven of nine portfolio tiles re-exported at USD 0. OBSERVED. (Note: this is reuse of Lab *media*, not of Lab *evidence*.)
3. **Micro-qualification before dependents** (learned in 001 SD-12, applied in 003): discarded-lineage share fell from 52.5% (001) to ≈ 26% (003); clip-2 built from the gated plate was accepted first draw. OBSERVED, n=1 each → INFERENCE.
4. **Pool-balance read before dispatch** (A7): in 003 the fal read (USD 0.147) blocked a ≈ USD 3.2 plan on a dead pool (`JOB.yaml:265`); in 001 the absence of this check dropped two video slots and killed the fallback (SD-11). OBSERVED.
5. **Frame-hygiene D1** after 001 SD-06 (Kling sharpened blur into letters): all 003 clips D1 pass on 12 sampled frames. INFERENCE (counterfactual unprovable).

**Added sophistication without a demonstrated CpAO/TTAO effect:**
1. **Capability Registry / routing map** (575 rows, 61 cells, 625 KB of YAML, USD 122): 001's accepted asset depended on a route "with no Registry cell" (SD-08); in 003 the route set was fixed by the user ("fal excluded", credits only) and pool balances, then annotated with cell statuses — the map described, it did not decide. No case cites a Registry row that changed a decision that would otherwise have been wrong. OBSERVED absence.
2. **Canon injection (2 packs, 21 check lines)**: 003's operator rendered PA-D1…D10 and CA-D1…D11 all "pass" (`JOB.yaml:154-174`), including PA-D7 "the hero image needs no copy" — then the human rejected V2 with "did cannon say nothing about product positioning? … canon had this knowledge. how's that possible?". The knowledge (Google ABCD "brand early, often and richly") is in accepted Canon (`canon/knowledge/current/google-abcd-video-ads/source-knowledge.yaml:667-669`) → it was **not retrieved** because `commercial_communication` is uncompiled (SD-07). State proved: knowledge exists → not retrieved. The check-line ritual produced false assurance (21 passes) rather than value.
3. **EVAL-037/038**: the repo's own tests. EVAL-038: weak model + the two packs lost **0/6** to a strong model alone (PM:203-215); EVAL-037's conclusion "Canon helps, but current retrieval/consumption is not mature". The plan-level value gate CANON-012 is "merged and closed" (CONTROL-STATE:85) — whether its 24 outputs were generated is UNKNOWN to me.
4. **Governance apparatus**: 117 decisions, 8 reviews, 10 audit docs, 6 history snapshots, 3 Governor refreshes — no production case cites any of them as changing a creative or routing decision; the only decision the operator uses is the in-session spend cap (`SKILL.md` "Prior authority is not reusable money").
5. **Per-job bookkeeping**: 10,000 words of JOB+LEARNING for an 18-s film; 3 sync PRs of 639–4,488 lines; 9 case files per job. The learning did transfer (003 applied 13 learning ids from 001/002, `JOB.yaml:96-108`) — but 003 still failed on three dimensions none of them covered.

---

## 3. The 80/20 (Q19)

If 80% of the repository were deleted, keep (by path, with the evidence for keeping):

| Keep | Why (evidence) | Bytes |
|---|---|---|
| `.claude/skills/media-agency/**` (5 files) | the only artefact that turns the repo into a production procedure; 003 ran end-to-end through it | 70 KB |
| `runtime/compositor/{gates.py,tokens.py}`, `runtime/loop/frame_hygiene.py`, `runtime/execute/{pools.py,provider_errors.py}`, `runtime/route/price.py` + roster pins, `canon/gate/` | the eight promoted deterministic gates (001 PROMOTION-QUEUE) + D1 + A7 — the components with observed defect-class elimination | < 1 MB |
| The per-job tools `tools/dispatch.py`, `tools/compose.py`, `overlay_text_video.py` (currently copied into each job dir on the job branches) | these, not `runtime/`, actually dispatched and assembled every production asset; `runtime/ALPHA-1.md:145-149`: "A live dispatch … does not exist" | small |
| `canon/compilation/PACK-*.yaml` (2) + `canon/packs/pack-triggers-v0.yaml` + `canon/CANON-SHAPE-v1.md §4-5` | the only Canon that reaches a job; keep until the strong-baseline test (§9) says otherwise | 107 KB |
| `production-learning/cases/**` + `tools/check_case.py` | the only empirical record of what fails in production; 003 consumed it | 164 KB |
| `eval/harness-v2/ledger.py` + `tests/test_ledger.py` + `test_authorisation_lineage.py` | the spend cap works and was the one process that prevented real failures | small |
| `coordination/CONTROL-STATE.md §6` (spend of record) + the 6 decisions of 14 Sep | current money authority; nothing else in `coordination/` is read by an operator | ≈ 60 KB |
| `UP/PROFILE.md` (the price list and the promise) | it is the product; the operator's intake is defined by it | 99 KB |
| Accepted media on the three raw branches (V4.1 film, nine tiles, Cumin accepted plates) | portfolio and reuse at USD 0 | — |

Delete or move out of git: `eval/experiments/**` sealed media (**2.31 GB** in the repo; keep manifests + the routing map's *summary* if the Registry survives §9), `canon/{findings,candidates,experiments,research}` (261k words of working prose), `history/**` (344 KB of byte-for-byte snapshots), `governance/reviews/**` (205 KB), `coordination/WORKSTREAM-STATUS.md` (a copy — the OS review said delete it; still here at 20.9 KB), the three `HANDOFF.md` (56.6 KB; `eval/HANDOFF.md` last edited **25 Aug**), `coordination/DECISION-LOG.md` (20 KB hand-curated, "not exhaustive"), `resources/**` (75k words, 51 MB), `docs/**`, and 111 of 117 decisions (archive). PROJECT-MEMORY.md becomes the ≤ 15 KB map the OS review specified — or is deleted in favour of the skill's BOOTSTRAP, which is the map that is actually used.

**INFERENCE:** the kept set is < 3% of bytes and ≈ 5% of markdown words, and every production asset to date was produced with exactly this subset (the Lab's 2.3 GB contributed three reused clips and a music bed).

---

## 4. Strong-baseline advocacy (Q12, Q75)

Method: for each verbatim brief I wrote what I (a current frontier LLM) infer with no repository context, then compared to what the operator actually decided in the job files.

### 4.1 Cumin — verbatim brief (`de1f978:…/JOB.yaml` brief.verbatim)
> "I am thiknig to make an ad for cumin. co. I would prefer making a video ad instead of image. … a video on how to hold chopsticks for them using their product images. they also wrote a blog post about it. preferably a short video, a very calm empathetic voice doing a voice over. A charchater trying to hold the chopsticks with a bowl or sorts from cumin co infront of him- mostly a young adult. the girl trying to explain him hoe to hold- step 1, step 2, step 3. the steps are visual with a very short text companion. the boy fails but they still happily eat through their cumin cookware."

**Baseline professional brief (no repo):** Proposition: "the bowl that makes noodle night easy" — a how-to that sells warmth, not instruction. Product role: hero in every frame; the bowl's own feature (rim rest/notch) is the closing product argument. Opening: a noodle slipping back into the bowl inside 1 s. Structure: 15–20 s, five beats — fumble / step 1 / step 2 / step 3 / laugh-and-eat — then a **product end card** (packshot on brand ground, product name, brand, URL). Proof: macro inserts of the grip, ≥ 3 s holds, big numerals. CTA/end card: mandatory for an ad; brand mark visible from beat 1 (Reels average watch < 3 s). Voice: one calm female Indian-English narrator, single source over silent clips, **lines generated and measured before the cut is locked**, ≤ 6 lines, brand said once aloud. Music: light, ducked. Hierarchy: text in the upper third clear zone, product lower-centre, Reels UI safe band. Platform: 9:16 master; 4:5 and 1:1 **re-framed from their own plates**, not cropped. Likely AI failure modes: hands/fingers/chopstick grip; open mouths under a VO reading as failed lip-sync; embossed logo garbled; text landing on the subject; VO overlap/overrun; identity drift between shots. Ask the customer: which product; spend cap; may the logo/embossed mark appear; spoon vs chopsticks ending; on-camera speech vs VO; Hindi?

**What the operator decided** (`JOB.yaml` blueprint/plan): nearly identical on concept, beats, hook, VO route, hierarchy, micro-qualification of the grip, closed-mouth risk (learned only after V1) — **and explicitly `cta: none in-frame`, `offer_placement: none`, no product end card, no brand mark before the last beat** (V1/V2). The human rejected V2 for exactly the end-card/opening omission.

**Delta.** *Machinery added:* frozen deck + code-set text (real), attempt ledger, per-geometry QA rows that correctly **flagged** the 4:5/1:1 crops as unable to carry copy (CF2 FLAGGED) — and then shipped them anyway. *Should have added:* the ABCD structure — sitting in accepted Canon, uncompiled. *Subtracted:* attention. Ten packs selected, two injected, 21 check lines hand-rendered "pass", a 10,000-word record, four intake questions — and the one structural rule any ad-literate baseline applies reflexively was missing. **Honest verdict:** the baseline would have made the *same* V1 mistakes (audio mix, mouths, text over figures, VO overlap) — those are execution/measurement failures no prior knowledge prevents; only gates do. The baseline would very likely **not** have omitted the end card and early brand. Net: on this job the Canon machinery was negative (false coverage), the gates were neutral-to-positive, and the difference-maker would have been two missing gates (VO schedule, subject obstruction) that cost nothing to write.

### 4.2 Upwork intro — verbatim brief (v2 brief paragraph, `UP/PROFILE.md:216-218` as quoted in `preprod/COMMERCIAL-BRIEF.md:178` @ f6ca66f; plus owner instruction 14 Sep: "fully AI-made", "a character speaking to camera", "crazy good because it IS the demo")
**Baseline professional brief:** 60 s, 16:9 (YouTube-hosted). Proposition: ad creatives in 24 h with the text exactly right, 4 h express. Opening: a finished ad on screen within 3 s while the first sentence is spoken (J-cut); a disclosed AI presenter for ≤ 20 s total, bookends. Structure: brief arrives → words approved → the ad builds itself → four sizes → six hooks + one Hindi flip → the QA catch (wrong digit fixed) → clips in motion → presenter close with the offer structure and the window qualifier → end card. Proof: real outputs, full-screen, ≥ 3 s each. Voice: Indian-English; presenter speech verified verbatim. Music: neutral bed, ducked. Failure modes: presenter identity drift across takes (anchor one still), lip-sync oddness, text hallucinated in generated frames, robotic TTS, cramped phone mock-ups, text clipping in composited cards. Ask: face or no face (conflicts with the live "not on the menu" line and Upwork's "video of you" rule), brand name spoken or shown once, hosting limits, may ads be generated for the film itself.

**What the operator decided:** V4.1 is this brief almost line for line (`PRODUCTION-MAP-AND-LEARNING.md` production map). But it took **five versions, 7 h 54 m, USD 15.39**, three analyst documents (112 KB) and **seven blocking questions** to the owner (`COMMERCIAL-BRIEF.md §11`) — five of which the baseline would also have asked. V1/V2 were rebuilt for creative direction the Controller only articulated after seeing them ("images AND videos are co-equal", "presenter is a HARD REQUIREMENT"); V3 failed on compositor engineering (text clipping, contrast, crops, card geometry) that no knowledge layer prevents. **Honest verdict:** the baseline would have produced a V1 of similar quality and made the same V3 engineering mistakes without gates; the machinery's contribution was the gates built *after* V3 and the sealed clips reused at USD 0. Canon (a 22.7 KB CANON-BRIEF) is not cited in any verdict as changing the film.

### 4.3 Portfolio tile 7 — verbatim brief (`UP/PROFILE.md:305, :504`)
> "Nivaas Homes | Real estate | Four-size set with price and possession date | Three-shot story (exterior, interior, offer card), Indian-English VO, 15 s | Three shots, one story, 15 seconds." / "Three-shot story clip (same people within the clip), Indian-English voice-over, plus WhatsApp still".

**Baseline professional brief:** three stills (exterior golden hour, interior, offer card composed by code with price/possession/RERA line) → three 5-s i2v clips **without native speech** → one TTS narrator generated once and split across the cut → code-set offer card → 9:16 + 1:1 + WA still. Failure modes: extend chains re-narrate and re-imagine; **two independent generations = two voices**; 720p softness on architecture; invented RERA numbers (use "RERA registered", no number). Ask: none needed for a portfolio tile beyond the copy approval.

**What the operator decided** (`REVISION-TRACE.yaml` N1/N2 @ 3bb9a3c): Veo t2v 8 s + **extend** with native narration (N1: 2.9-s hole inside a sentence, soft 720p) → then two i2v clips with native narration (N2: two different voices). Both risks were already recorded in case 001 (RO-01 extend restructures narration; RO-05 voice) and the workflow was bypassed (PD-01…09). **Honest verdict:** here the repository *knew* and the baseline would have *guessed right* (single TTS source is common knowledge); the failure was neither knowledge nor model but process bypass under time pressure — the same morning the workflow was merged.

**Summary of the delta across the three:** what the machinery reliably added was *measurement* (exact text, ledger, geometry rows, frame sampling) and *reuse*; what it did not add was the professional structure a strong baseline supplies for free; what it subtracted was operator attention (per-job bookkeeping ≈ 10k words, 21 check lines, 24 bootstrap documents) and, in 003, confidence ("packs injected", "PA-D7 pass") that the structure was covered when it was not.

---

## 5. Cognitive-load audit (Q72) — expert work pushed back onto the human

Counted from the job files; a "decision point" is a question the human had to answer or a verdict the human had to give before work could continue.

| Case | Questions asked of the customer/owner | Verdict/gate rounds | Defects the human had to find | Total decision points |
|---|---|---|---|---|
| 001 | **7 blocking questions** (`COMMERCIAL-BRIEF.md §11`: character, who is "I", brand spoken/shown, tile direction Ledge/Wall/Price-Card, clock, hosting, ads-before-tiles) + script v5 "for approval before any generation" | 5 version verdicts | 25 | **13** |
| 002 | 3 confirmations requested in the handover (`portfolio-export/README.md`: Hindi CTA "confirm", two draft copy decks) + 3 "go" decisions (story tile, two stills, motion) | 5 review cycles (B1 defects, B2, N1, N2, B3) | 13 | **11** |
| 003 | 4 intake questions (`JOB.yaml:66-70`: cap, freeze deck, pool attestation, spoon-vs-fist ending) | **8 pre-assembly gate verdicts** (plate H1 r1/r2, clip-2, plates A/H2/H3, plate-B, voice rounds 1–5 = 26 takes judged by the user's ear) + 3 version verdicts | 8 | **15** |
| Total | 14 | 25 | **46** | **39** |

Specific instances of expert work delegated upward:
- **Plate choices asked** (003: "r1 or r2?" on plate-H1; plates A/H2/H3/B; `HUMAN-VERDICTS.yaml:5-17` @ 1de2b37) — a creative director chooses plates; the customer should see the film.
- **Voice casting by the customer's ear** (003: five rounds, 26 takes across Sarvam/ElevenLabs/Gemini; `TIME-AND-COST.yaml` "the voice search … dominated") — pushed to the human because no route was pre-qualified for a calm Indian-English female read despite USD 122 of Lab spend.
- **Pool liquidity attestation** (003 A7: "I attest all pools cover the cap") — the system asked the human to vouch for balances it could not read.
- **Ending decision "spoon vs fist-grip"** (003) — a defensible ask; the rest were not.
- **Tile direction "Ledge / Morning Wall / Price Card"** (001 Q4) — a design choice pushed to the owner before anything was rendered.
- **QA by the customer**: 46 defects found by the human vs 3 by gates/operator before presentation. In 002 the customer wrote ten defect messages in 19 minutes (`HUMAN-VERDICTS.yaml` B1).
- **ACCEPT-only release** (C-8) is right in principle, but combined with the above the human is simultaneously client, art director, casting director, QA and treasurer.

---

## 6. Anti-bureaucracy ledger

### 6.1 Processes whose cost exceeds the failure they prevent (evidence)
1. **Governor refreshes + byte-for-byte snapshots.** Three "Governor refresh" commits (3, 8, 14 Sep) and 6 commits into `history/` (**4,149 inserted lines**; 344 KB), plus **11,317 lines inserted** into the four state docs over their life. Outcome: PM regrew 18.6 → 38.4 KB and CONTROL-STATE 12.9 → 30.1 KB after the migration that was meant to fix exactly this. No post-28-Aug incident of a worker acting on stale state is recorded (UNKNOWN whether any occurred) — the ritual's benefit is unmeasured; its cost is measured.
2. **Sealed-evidence rituals.** 35 commits with "seal" in the subject; **2.31 GB** of media in git; `verify_sealed_evidence.py`; a 14-Sep evidence-rulings decision. What production consumed from it: three clips and a music bed (USD 0 reuse) and route *labels*. The Registry's 575 rows produced no cited routing decision in three jobs.
3. **Ledger reconciliation.** A 28k-word audit pair established that the ledger is an upper bound, found two cap crossings of **USD 0.40 and 0.31**, and then shipped budget-lineage arithmetic, a replay test and a vendor-statements schema — while the four vendor statements have still "not been read" (`AUDIT…SPEND-RECONCILIATION.md:169-172`). The machinery to prevent a ≈ USD 0.71 overrun cost more than the overrun by any accounting.
4. **117 Controller decisions** (77,131 words) in 23 days, 64 of them in three days; the decision index is hand-curated and "deliberately not exhaustive" (RUNBOOK:132-134). An operator reads none of them except the spend cap.
5. **Stale handoffs kept.** `eval/HANDOFF.md` 32.6 KB, last commit **25 Aug**; `resources/HANDOFF.md` 28 Aug. The OS review's "≤ 2 KB stubs" was not done; the mitigation ("not compulsory") leaves 56.6 KB of provably stale prose as a trap.
6. **Per-job bookkeeping and sync PRs.** 10,000 words of job record for an 18-s film; a 9-file case per job; PR #98 = 93 files / 4,488 lines, #100 = 902, #103 = 639. The learning transfer is real (003 cites 13 learning ids) but the *form* — YAML with `null`/`unknown` discipline, sha256 per asset, two-clock time files — is auditor-grade for a USD 5 job.
7. **Check-line rendering as compliance theatre.** 21 lines hand-marked "pass" in 003 (`JOB.yaml:154-174`), including PA-D7 on the very dimension the human rejected. Cost: operator attention; benefit: none observed (SD-07).
8. **Communication-check ritual and two-layer (Founder/Controller) reports** (RUNBOOK:40-48, :113-127): a fixed per-session token tax with no measured effect.
9. **The Capability Lab itself** (USD 122, 2 days, 35 cases, 575 rows) against the 28-Aug advice of USD 30–40 need-driven: its production yield is §6.1 item 2.

### 6.2 Processes that DID prevent real failures (evidence)
1. **Spend caps + pool reads**: A7 blocked a dead-pool plan (003); all three job caps held (15.39 under INR 5,000 records; 4.66; 5.09 of 8); EMP-001/EVAL-038 under USD 10 caps. 001 SD-11 shows what happens without the pool read.
2. **Frozen copy deck + code-set text**: zero exact-text defects in three cases — the single promise the profile sells ("text rendered exactly as you send it, every time").
3. **Micro-qualification** (003): discarded-lineage spend halved vs 001.
4. **Attempt ledger with failed calls included**: made every number in this report computable; caught the id collision (DF-06) and the quota failure (att-038) as records rather than mysteries.
5. **Frame sampling (D1)** and **provider-error classification** (SD-09/10 → `provider_errors.py`): 003 shows no signage hallucination and correctly classed the Gemini refusal.
6. **Format-specific revalidation** (from 002): in 003 it *flagged* the 4:5/1:1 crops (CF2) — the process then failed by shipping flagged files, not by missing them.

---

## 7. Would a skeptical agency owner pay for this pipeline? (10 jobs/month at Upwork prices)

Assumptions stated; all price inputs from `UP/PROFILE.md:215-241, :279-284` and `UP/ACCOUNTABILITY.md`.

**Job mix (10/month):** 4 × Static Starter $60, 3 × Video Starter $75, 2 × Static Standard $120, 1 × quoted film $300 → gross **$1,005**; after Upwork 10% ≈ **$905**.

**Pipeline economics (observed inputs):**
- Provider cost/job: mean 8.38 (range 4.66–15.39); statics far lower (≈ $0.6 per new static tile in 002). Take **$50–85/month**.
- Fixed: Claude Max **$200/month** (ACCOUNTABILITY.md), Connects ≈ $15–45.
- Owner review time/job (the scarce input): 001 ≥ 3 h 50 m of gaps + 5 verdict exchanges; 002 ≈ 1 h; 003 ≈ 3 h working span + 10 cycles. Take **3 h/job = 30 h/month**.
- Contribution before owner time: 905 − (200 + 68 + 30) ≈ **$607**. At the profile's own $35/h the owner's 30 h = $1,050 → **net ≈ −$440/month**. Break-even requires ≤ 17 h/month of owner time (**1.7 h/job**). Only case 002 — the one that bypassed the workflow and re-exported accepted plates — came in under that, and it shipped 10 defects.
- The ACCOUNTABILITY floor ("USD 250 net after Connects + Claude + pipeline, from month 1") is arithmetically reachable only if the owner's time is valued at zero **and** ≥ 6 orders land in month 1; as of 15 Sep, 0 proposals have been sent.

**Alternative: one creative director + one producer/editor with direct tool access** (Veo/Nano Banana/CapCut/Figma; Gurugram contract rates, HYPOTHESIS: CD ₹1.5–2.5 L/month ≈ $1,800–3,000; producer/editor ₹50–80k ≈ $600–950; tools $100–200): **$2,500–4,150/month fixed**. At 10 jobs/month × $100 that is −$1,600 to −$3,200 — worse. Their break-even is ≈ 30–45 jobs/month at these prices, at 2–4 h/job, which a two-person team can physically do. A single freelancer with direct tool access (the actual Upwork competitor: `UP/PROFILE.md:444` "TR+ statics $40–47 per static … 2–3 day delivery") does a $75 clip in 2–4 h with no fixed cost beyond tools.

**Skeptical owner's verdict (INFERENCE):** Neither configuration is viable at new-seller Upwork prices and 10 jobs/month. The pipeline's only structural advantage — near-zero marginal cost — is real (≈ 1–7% of price) but irrelevant while the scarce input (senior judgement hours per job) is **not reduced**: three cases show 1–8 h of owner time per job, i.e. the same hours a competent human would spend *making* the thing, spent instead *reviewing* it and finding 94% of the defects. He would not pay for "the pipeline". He would pay for ≈ 6 gates, the exact-text compositor and the ledger as tools in the hands of one creative with direct tool access — the §3 subset.

---

## 8. Reliability — single points of failure hit in production

| SPOF | Where it hit | Handled by the architecture? |
|---|---|---|
| **Credits/pool exhausted** | 001 SD-11: fal cash 3.23 → 0.26 mid-job; video slots dropped, Wan fallback "structurally dead". 003: fal cash **USD 0.147** vs a ≈ 3.2 plan (`JOB.yaml:265`); ElevenLabs **quota_exceeded, 54 credits vs 159 required** (att-038). | 001: **no** (discovered by failure). 003: **yes** — A7 read blocked fal before spend; ElevenLabs failure was ledgered and the route abandoned. But balances for Vertex/Gemini/Sarvam are "not readable by API" → the system asks the human to *attest*. Partially handled. |
| **Attempt-id collision** | 003 DF-06: two concurrent dispatches computed `att-019` (ids from a line count, no lock) | **Worked around** (alias ledger line), **not fixed** (candidate ATTEMPT_ID_LOCK). Concurrency is unsafe today. |
| **Model refusals / outages** | 001 SD-09 Veo gRPC 14 UNAVAILABLE ×2 (succeeded 100 s later); SD-10 Lyria 503/500/500 on the frozen prompt (neutral rewrite succeeded); 003 att-045 Gemini TTS `PROHIBITED_CONTENT` on the frozen line "Pinch… and… nearly." (regenerated); Lab: six Wan 422s ledgered as USD 2.88 spent though "nothing charged". | **Yes, after 001**: `provider_errors.py` classifies transient vs refusal; retries are ledgered. The Lab's ledger-vs-bill gap is a known, unresolved accounting SPOF (§6.1 item 3). |
| **Tool 10 MB limits** | **No evidence found** in the three job trees or cases (`git grep -i '10 ?MB'` on all three refs: no hits). | UNKNOWN — if it occurred it was not recorded; the lead should treat the claim as unverified. |
| **Live dispatch outside the runtime** | Every production asset was dispatched by per-job scripts (`tools/dispatch.py`, `compose.py` copied into the job dir); `runtime/ALPHA-1.md:145-149`: live dispatch "does not exist". 97 runtime .py files / 34 tests sit beside the real path. | **Not handled**: the tested code is not the code that runs; the running code is untested and re-copied per job (003 att-001 "operator tool bug … nothing sent"). |
| **Single human as release authority + QA instrument** | 46 of 49 found defects were found by the human | By design (C-8) — but it makes the owner the throughput limit (§7). |
| **Chat-only evidence** | Every human verdict in three cases is "chat_only_human_evidence"; ACCEPT minutes unrecorded (001, 002) | Not handled; TTAO is a lower bound in every case. |
| **VO scheduling / subject obstruction gates absent** | 003 V1 and V3 rejected on dimensions "no gate measured" | Promoted as `check_vo_schedule` in PR #103 (not yet on main). |

---

## 9. What evidence would convince me to simplify (Q20) — and does it already exist?

It exists. Six independent lines, all in the repository:
1. **Three cases, one tally:** model failures 0/25, 2/13, 1/8 of what reached the human — the pipeline around the models, not the models, is what fails (`SYSTEM-DEFECTS.yaml` ×3). Every promoted fix is a small deterministic gate; none is a Canon rule or Registry row.
2. **The repo's own strong-baseline test:** EVAL-038, weak model + the two packs vs strong model alone: **0/6**, all 18 top-3 slots to the no-Canon baseline, cheaper per package too (PM:203-215). EVAL-037: "retrieval/consumption is not mature".
3. **Cumin:** the human's rejection ("canon had this knowledge, how's that possible?") is answered by `canon.missing_domains: 8 of 10` — and the missing knowledge (ABCD) is in any frontier model's prior.
4. **Case 002** — the bypassed workflow — has the best TTAO (1 h 07 m) and lowest per-tile CpAO of the three, while case 003 — fully conformant — failed. Conformance is not correlated with acceptance at n=3.
5. **The state layer regrew** (PM +106%, CS +133% in 18 days) despite an explicit migration; the OS review's growth-law test failed within three rounds.
6. **Spend allocation:** 84% Lab / 16% production; the Lab's 575 Registry rows are not cited as deciding any production route; the accepted intro film's key route had no cell.

What would *not* yet justify deleting the gates: they are the only components with observed defect-class elimination (§2.4). What is still missing and would settle the Canon/Registry question: the project-head review's Round 1 (A raw prompt / B′ strong LLM + length-matched craft context + the six gates / E full stack) on 8 real briefs, blinded — never run. Cost ≈ USD 30–60 at 003's rates. Until then the honest position is: **the gates and the ledger earned their keep; nothing else has evidence of reducing CpAO or TTAO, and the reading burden and bookkeeping have measured cost.**

---

## 10. Prior-review adoption scorecard (28 Aug → 15 Sep)

| Recommendation (source) | Status | Evidence |
|---|---|---|
| Split PROJECT-MEMORY → map + `history/` (OS §F) | **Adopted** 28 Aug (`511eda7`), then eroded | 105 KB → 18.6 KB → 38.4 KB |
| CONTROL-STATE ≤ 15 KB, sole state doc (OS §E1) | Adopted then breached | 12.9 KB → 30.1 KB (above the pre-migration 21.7 KB) |
| Fold in and delete WORKSTREAM-STATUS (OS §F) | **Not adopted** | 20.9 KB, last edited 14 Sep |
| Handoffs → ≤ 2 KB stubs (OS §F) | Not adopted; mitigated | RUNBOOK:65 "NOT compulsory"; `eval/HANDOFF.md` 32.6 KB, 25 Aug |
| Task template: named sections, expansion triggers, STOP on insufficiency (OS §E2) | **Adopted** | `shared/CONTEXT-SUFFICIENCY-POLICY.md`, template lines 11-13 |
| `verify/run_all` + CI + check log (OS §E3) | Partial | `verify/VALIDATOR-INDEX.yaml` ("not a CI system"); no `.github/workflows`; no check log |
| Two-tier Governor; deep audit scheduled not default (OS §E) | Partial / inverted | GOV-L1 reviews stopped 30 Aug; replaced by 3 "Governor refresh" commits + 2 audits (28k words) + snapshots |
| One strategy change → one state commit (OS §H) | Not met | 16 PM commits + 46 CS commits since `a89af60` |
| Pilot first, before more Lab (PH §3, §6) | Adopted **after** the Lab | Lab 8–10 Sep (USD 122); pilot 14 Sep |
| Need-driven admission ≈ USD 30–40 (PH §4 Task 2) | Not adopted | USD 122, 35 cases, 575 rows |
| No further capability investment without a demand signal (PH §7) | Not adopted | same |
| No GOV-007, no handoff refresh until after Phase 3 (PH §7) | Letter yes, spirit no | no GOV-007; refresh rituals continued |
| Round-1 A/B′/E blinded architecture test with pre-committed kill rule (PH §5) | **Never run** | — |
| Cap PROJECT-MEMORY growth (PH §7) | Failed | above |
| Frozen human-review protocol before outcomes (PH §4 Task 0) | Not adopted for production | all verdicts chat-only, unblinded, un-timestamped |

---

## Findings ranked

1. **The models are not the bottleneck; the system around them is.** 43 of 46 defects that reached the human across three cases were pipeline/compositor/creative-direction/process failures (OBSERVED). Every effective fix was a ≤ 100-line deterministic gate.
2. **Process mass dwarfs product mass.** 207k words of governance prose vs 16k words of operator creative guidance (12.9:1); 43% of 899 commits governance-tagged; 117 decisions; 84% of provider spend in the Lab. Production output to date: one accepted film, nine tiles (seven re-exports), one rejected spec, USD 0 revenue.
3. **Canon did not reach the job where it mattered.** 2 of 10 packs compiled; the rejected dimension in Cumin (ad structure) sits in accepted Canon, uncompiled, and in every frontier model's prior. The repo's own EVAL-038 shows packs + weak model losing 0/6 to a strong model alone.
4. **The 28-Aug recommendations were adopted in form and defeated by regrowth**: PM/CS doubled again within 18 days; WORKSTREAM-STATUS and 56 KB of stale handoffs persist; the need-driven Lab cap was exceeded 3–4×; the blinded architecture test never ran.
5. **Owner time is the unpriced cost that kills the economics.** 1–8 h per job, 39 decision points and 46 defects found by the human in three jobs; break-even at Upwork prices needs ≤ 1.7 h/job. The only sub-2-h job bypassed the workflow.
6. **What worked and should be kept**: spend caps + pool reads, frozen deck + code-set text, micro-qualification, attempt ledger, frame sampling, error classification, format revalidation (§3 subset, < 3% of bytes).
7. **Reliability**: pool exhaustion (handled after 001), attempt-id collision (worked around, not fixed), refusals/outages (classified after 001), no live dispatch in `runtime/` (the running code is per-job, untested), chat-only verdicts. No evidence of a 10 MB limit incident.
8. **Spend accounting is an upper bound, not a cost**: vendor statements unread after two audits; EVAL-037 (USD 3.23) absent from the spend of record; EVAL-038 ledger reserve sum (3.96) ≠ CONTROL-STATE (2.26).

## Open questions / unknowns
- **LLM/operator reasoning cost per job**: not recorded anywhere (subscription-metered). CpAO numerators are provider-only lower bounds.
- **Vendor-billed totals** for every pool: never reconciled; all USD figures are ledger reservations at pinned prices.
- **Did CANON-012 (plan-level value gate) ever generate its 24 outputs?** CONTROL-STATE:85 says "merged and closed"; I did not locate a result and did not chase it.
- **Any post-28-Aug incident of a worker acting on stale state?** None recorded; the Governor-refresh benefit is therefore unmeasured rather than zero.
- **The "10 MB tool limit" SPOF** named in my brief: no trace in the three job trees or the cases; treat as unverified.
- **Owner minutes per job** are inferred from unattributed gaps and chat timestamps; no case records them directly (001 explicitly "not measured").
- **Alternative-team cost** (§7) is a market HYPOTHESIS, not repository evidence.
- **EVAL-038 spend**: which of 2.26 / 3.96 the vendor billed is unknown; the conflict is reported, not resolved.
