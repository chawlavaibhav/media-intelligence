# External PM Review — Video-Gen Market and Programme Critique — 2026-08-28

**Status:** ADVISORY INPUT ONLY. Commissioned by the Controller from a research agent playing a
senior engineering-PM-at-a-frontier-video-company role. It authorises nothing and creates no
project fact by itself. Where it conflicts with committed evidence or durable Controller
decisions, they win.

**Verification caveat:** all market prices below are reported from secondary web sources
(accessed 2026-08-28), not verified on primary provider pages (sandbox egress blocked several).
Every price remains subject to the project's mandatory execution-time route/price verification.
Repo claims cite file paths and were checked against `main` at the time of writing.

---

## A1. Video-gen model/API landscape and pricing (Aug 2026, reported)

| Model / route | Reported price | 9:16 | Native audio | Image-conditioning | Notes |
|---|---|---|---|---|---|
| Veo 3.1 Fast (Gemini API, fal) | $0.10/s 720p/1080p no-audio; $0.15/s with audio | yes | yes (optional) | yes — first frame, first+last frame, up to 3 reference images | Current project route; $0.80/8s matches market. |
| Veo 3.1 Standard | ~$0.40/s 720p (reports conflict, up to $0.75/s Vertex) | yes | yes | yes | UNVERIFIED — check at dispatch. |
| Veo 3.1 "Lite" | $0.03–0.05/s 720p (reported only) | ? | reported yes | ? | Existence/price NOT verified on any Google page. If real, most important number for ₹99 economics. |
| Runway Gen-4.5 | $0.12/s ($0.60/5s); $10 min top-up | yes | not reported | i2v yes | 720p, 5s/10s clips. |
| Kling 2.5 Turbo / 2.6 / 3.0 | ~$0.31/5s (~$0.06/s) via resellers; official API prepaid credits | yes | 3.0: yes | t2v, i2v, multi-shot (up to 6 shots/15s), reference-based | Kling 3.0 strongest multi-shot story tool; cheap tier among best $/s. |
| Hailuo / MiniMax | ~$0.01/s 512p, ~$0.04/s 768p, ~$0.08/s 1080p (reseller-reported) | yes | — | i2v yes | Cheapest credible plate at 768p (~$0.32/8s). |
| Wan 2.5 (Alibaba) | $0.05/s 480p, $0.10/s 720p, $0.15/s 1080p on fal | yes | 2.5+ reported audio | i2v yes | Open-weight lineage → self-host path exists. |
| Luma Ray-2 / 3.x | Ray-2 ~$0.08/s; Ray 3.2 credit-priced | yes | — | i2v yes | Strong camera moves from keyframe. |
| Pika 2.5 | subscription-first ($35/mo std) | yes | — | i2v yes | Weak API story. |
| Sora 2 / Pro | **API sunsets 2026-09-24; app discontinued 2026-04-26** | — | — | — | DO NOT build on Sora. |
| Seedance 1.5/2.0 | 2.0 Fast reported ~$0.09/s | yes | 2.0 Fast no audio | i2v yes | Credit-priced on aggregators. |
| Aggregators (fal.ai, Replicate) | pass-through per-second | — | — | — | fal is the practical multi-model tap; T2 harness + provider-redundancy hedge. |

Sources (accessed 2026-08-28): fal.ai/models/fal-ai/veo3.1/fast · buildmvpfast.com/api-costs/ai-video ·
costgoat.com/pricing/google-veo · aifreeapi.com/en/posts/veo-3-1-pricing · renderful.ai/blog/kling-api-pricing ·
piapi.ai/kling-2-6 · kling.ai/quickstart/klingai-video-3-model-user-guide · apiframe.ai/guides/runway-api-guide ·
developers.openai.com/api/docs/deprecations · help.openai.com/en/articles/20001152 ·
evolink.ai/blog/wan-api-pricing-guide · eesel.ai/blog/luma-ai-pricing ·
atlascloud.ai/blog/guides/cheapest-ai-video-generation-api-2026 · getimg.ai/blog/google-veo-3-1-review ·
cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1

**Two facts that matter most:** (1) Veo 3.1's image-conditioning (first frame / first+last /
3 reference images) is available on the same route already integrated in EVAL-035 — image-first
needs no provider change. (2) There is a 3–8× price spread between Veo Fast and cheap-tier plates
(Hailuo 768p, Kling turbo, Wan 480/720p) for the same 8 seconds; whether the cheap tier passes
"premium" is exactly the empirical question T2 must answer. Nobody publishes accept-rate-per-dollar.

## A2. Image-gen text rendering, incl. Devanagari

- 2026 marketing claims GPT Image 2 "solved" text (~99% character accuracy incl. Hindi); roundups
  put GPT Image 2, Seedream 4.5 ($0.04/img) and Ideogram at the top.
- The project's own sealed evidence contradicts the marketing at the exactness standard:
  GPT Image 2 6/8 exact, Ideogram v3 1/8 (`eval/empirical-tranche-1/evidence/EMP-001/atex-scoring/`).
  "99% character accuracy" and "exact string, zero tolerance" are different standards; no vendor
  publishes exactness-standard numbers at all.
- Practitioner state of practice is exactly this project's architecture: generate the visual,
  overlay text/logos deterministically in brand fonts. Deterministic text is table stakes done
  properly; the differentiator is *certifying* it (see A5).
- Image price floor for the ₹9 product: Imagen 4 Fast $0.02, Ideogram 3.0 $0.03,
  Nano Banana 2 Lite ~$0.034, GPT Image 2 low $0.005–0.03 / medium $0.041 (reported).

## A3. What production ad-creative products ship and charge

- **Creatify** — templates + avatars + gen models; effective ~$1.65 per 30s ad on Pro tier.
- **Icon.com — the most important market signal:** retired its AI ad-maker in 2026 and pivoted to
  human-made UGC ("The Human Admaker", $1,000/mo for 6 ads ≈ $167/accepted ad). A funded team
  concluded pure-AI output couldn't hold acceptance quality — a direct market datum on exactly the
  H1/H6 failure PILOT-001 Candidate 1 hit.
- **HeyGen** — avatar-first, ~$1/min effective at tier price.
- **Higgsfield** — aggregator suite; practitioner-estimated true cost **$0.60–1.00 per *usable*
  Kling-quality clip and $3–9 per *usable* Veo/Sora clip once re-rolls are counted** — the closest
  published thing to a CpAO: implied first-pass accept ~20–35% on premium models for prosumer T2V.
- AdCreative.ai and Captions 2026 pricing could not be retrieved — unverified.
- Pattern across all of them: brand-kit/template layers composited deterministically over generated
  or stock visuals; the gen model supplies the plate/avatar, never the type. PILOT-001's P1–P4 is
  structurally the same pattern.
- "Accepted outcome" reference prices: MKT-002's real buyer pays $30–45 per approved video
  (`canon/research/marketplace-demand-v1/derived/COVERAGE-REPORT.md`); Icon $167/ad human-made;
  Creatify ~$1.65 self-serve. ₹99 (≈$1.04) sits between self-serve-slop and approved-outcome
  pricing — a wedge or an underpricing mistake; T2 decides which.

## A4. Practitioner patterns for reliable short ads

1. **Image-first is the default professional workflow.** Generate keyframes with a cheap
   controllable image model, human-select, then image-to-video. T2V is for exploration; I2V is for
   production — the visual anchor pins product, palette, composition, brand.
2. **One prompt = one scene = one camera move.** Timed multi-phase choreography inside one 8s clip
   is known to fail. The Attempt-2 supersession decision independently rediscovered at $0.80 what
   the practitioner literature says for free — that literature is minable into Canon at zero API cost.
3. **Longer pieces are stitched** from per-shot generations with continuity via reference images /
   first-last-frame bridging, not one narrative prompt.
4. **Brand assets are composited, never generated.** Negative space for typography is planned at
   the keyframe stage.

Bottom line: P1–P4 is state-of-practice **except** the project entered at T2V; the market entered
image-first, for the same reason Candidate 1 failed.

## A5. Evaluation

- VBench / VBench-2.0 is the de-facto academic standard for automated video-gen evaluation —
  benchmarks *models*, not *outcomes*; useless as an accept gate for a specific deliverable.
- No product found that certifies exact on-screen text automatically as a guarantee (video-OCR QA
  tooling exists as generic test automation). Absence-of-evidence flag: cannot prove nobody does
  it, only that nobody markets it.
- The project's mechanism finding (recognisers repair misspellings; literalness vs accuracy are
  opposing virtues) plus deterministic composition is a credible path to a "certified exact claims"
  guarantee nobody else offers. **That is the moat candidate, not model choice.**

## B. Programme critique (summary)

1. **T1→T8 broadly right.** Cut the architecture experiment from 6 arms to 3 first (raw prompt /
   strong LLM / IR+production-intelligence); add Canon arms only if IR+PI beats the naked LLM.
   Merge keep/kill into the experiment readout. Highest over-engineering risks: eval-lab
   re-inflation at T6 and governance mass. Fix without process: spend in tranche envelopes
   (~USD 25–50 per decision), enforced by the existing mechanical ledger.
2. **Deterministic overlay: unambiguously right** (12/12 hard checks first try). **T2V plate: wrong
   default** — a keyframe gate inspects composition/negative-space/premium-ness on a ~$0.04 still
   before paying video price. T2 must screen image-first→I2V as primary arm, pure T2V as control.
3. **Minimal T2 screen:** 3 briefs (Aight + MKT-005 + MKT-012), 3 phases — keyframe screen (~$1.5,
   3 image models), I2V plate screen (~$18, 4 video routes + T2V control), composite + blind
   frozen-rubric human scoring ($0). **USD 25 envelope, one spend decision.** Metric: first-pass
   accept rate per dollar per route per workflow.
4. **CpAO reference points (USDINR ≈ 95.5):** ₹99 video needs CpAO ≤ $0.45–0.50 for ~50% gross
   margin → cheap plate ($0.32–0.50) × ~1.3 mean attempts (≥75% first-pass accept, bought by the
   keyframe gate) + keyframe + checks. Veo Fast at $0.80/attempt is 77% of revenue at perfect
   acceptance — premium-tier only. PILOT-001's actual 2-attempt trajectory ($1.60) is 154% of
   revenue. ₹9 image: $0.02–0.04 generation + $0 overlay + ~$0.0015 OCR ≈ 45–65% gross margin —
   comfortable. HED-1 is not academic: at ₹99, even 2 minutes of per-unit human review is material;
   runtime v0 needs batch/spot-check human gating.
5. **Top risks:** creative acceptance rate (the H1/H6 wall — what killed Icon's AI product);
   unit economics at premium-plate prices; demand mismatch (runnable-16 skews to identity/avatar/
   supplied-asset work, only 1/18 wants exact text); provider churn (Sora dead, `-preview` model
   ids); single-human accept gate (founder taste unaudited — test with a 3-person external
   micro-panel against the frozen rubric).

## C. Prioritized post-T1 actions (headline)

1. Write PILOT-001's actual fully-loaded CpAO line ($0) — forces HED-1 open.
2. Keyframe screen (~$1.50).
3. I2V plate screen + blind scoring (~$18; single USD 25 envelope).
4. Execution-time price-sheet for shortlisted routes only, incl. verifying the reported Veo "Lite" ($0).
5. Devanagari deterministic-overlay proof via benchmark-qualified Cloud Vision (~$0.02).
6. MKT-014 supplied-still animate attempt (~$0.50–0.80) — demand-generalisation probe.
7. External 3-reviewer micro-panel on Candidates 1/2 + T2 batch ($0–20).
8. Harden deterministic composition into parameterized brand-token templates ($0) — seed of
   Production IR extracted from real recipes.
9. fal.ai standby smoke call (~$1) — provider-churn hedge.
10. Demand-to-capability desk map ($0) — makes T6 evaluator qualification demand-driven.

Total ≈ USD 25–45. Constraints respected: no Planner before Registry evidence, no Registry rows,
admission bar untouched.

**Closing opinion:** the project's discipline is its asset and its risk. The deterministic-text
moat is real and unclaimed. But companies died here on creative acceptance rate, not rigor — and
acceptance rate is bought with cheap iterations: image-first, cheap plates, tranche-level spend.
Spend the next $25 learning accept-per-dollar; everything else can wait.
