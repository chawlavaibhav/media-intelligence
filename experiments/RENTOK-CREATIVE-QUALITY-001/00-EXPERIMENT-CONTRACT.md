# RENTOK-CREATIVE-QUALITY-001 — experiment contract

Opened 2026-09-21 (IST morning) by the Media Intelligence Controller session (Claude Opus 5), Writer for this experiment's records only, on branch `work/experiment-rentok-creative-quality-001` from `origin/main @ c88c0d5`. Human Controller and customer of record: Vaibhav Chawla. No sealed experiment, accepted job record, `canon/**`, `eval/registry/**`, `eval/capability-map/**` or `coordination/**` is modified by this experiment.

## 1. Customer feedback of record (verbatim from the Controller task, 2026-09-21)

> ChatGPT direct executions: Both versions were technically functional but creatively poor. The modern revision did not reach the desired standard.
> Repository Lane B — ChatGPT-directed, Claude-executed: Technically and creatively acceptable, but not a great video.
> Repository Lane A — autonomous five-stage question-answering pipeline: Better overall and accepted, but still below the desired creative standard.
> The customer believes that the question-answering process has improved the result. However, the final creative quality remains insufficient.
> The customer also reports that earlier Media Factory experiments produced stronger videos.
> The customer's hypothesis is that creative intelligence may be lost between planning and the final model-facing prompt.

The hypothesis is tested, not adopted. Acceptance of the two films (RENTOK-GAME-A-004 / B-005, PR #104 open, not merged; PR #103 open, not merged) is not evidence that the creative-quality problem is solved.

## 2. Question and candidate causes
Why does the pipeline produce technically correct, acceptable media below the desired creative standard? (A) creative direction under-ambitious or mis-specified · (B) creative information lost in translation to asset prompts / animation instructions · (C) the selected production method (AI stills + code animation) cannot realise it · (D) a combination. Three prompt kinds are kept distinct throughout: asset-generation prompt · animation/compositing instructions · video-model prompt.

## 3. Design
Phase 1 (USD 0): reconstruct the actual Lane A chain (brief → questions → Canon → plan → prompts → render code → media), the loss-of-intent trace, the Media Factory evidence, the frozen baseline (Treatment A: the ≈ 5-s power-up + first-clear sequence cut from the accepted Lane A final, no regeneration), a priced plan and a blind evaluation protocol.
Phase 2 (paid, under a cap the human Controller states in writing): Treatment B (asset-prompt only; everything else frozen) · Treatment C (stronger creative direction, same renderer where feasible; renderer limits documented, objective never weakened) · Treatment D (production-method alternative using C's direction: image-/reference-to-video on credits, micro-qualified first). Smallest unit first; stop and inspect before each further spend; failed attempts kept and counted; no full 30-s film in the diagnostic phase.
Phase 3: independent blind evaluation of the four clips (media only); diagnosis by cause (A/B/C); proposed route to extend the strongest treatment to the full ad, with capability risks.

## 4. Controls
Baseline assets, render code and settings frozen by sha256 before any comparison. Treatment B changes exactly one variable class (asset prompt); C changes direction + renderer code (recorded); D changes the production route — reported as a route comparison, never as a prompt-only result. Same narrative event, ≈ 5 s, same customer-quality objective across treatments. Spend: credits only, no fal, no new paid service; cap recorded in `SPEND-AUTHORISATION.md` before the first paid call.
