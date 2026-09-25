# How generative-media companies manage creative context at scale

Research appendix 03 of `CONTEXT-SOLUTION.md`. Compiled 2026-09-25 from primary sources (product docs, help centres,
API docs, engineering blogs, arXiv, a Latent Space interview, the Google Marketing Solutions GitHub repo). Some pages
blocked fetching (Midjourney docs, Runway help, Adobe helpx, Canva newsroom); claims marked **(snippet)** rest on
search-result text. **[Inference]** = our reading, not a sourced claim. "Runway, Hagen, Hicksville" = Runway, HeyGen, Higgsfield.

---

## Part 1 — What each company actually does

### Runway
- **Every production model rewrites prompts behind the scenes.** Anastasis Germanidis (co-founder, then CTO) on Latent Space: "every single like, video generation
  model in production uses a complex prompt completion pipeline under the hood". Users "wanted a lot more control than
  that, so we invested in control building on top of those models very quickly" (Motion Brush, camera control, first-frame
  conditioning, depth-to-video). https://www.latent.space/p/runway
- **The video agent is an LLM calling tools.** It is an "LLM that is very effective at tool use of different image models, video models" across
  the workflow, including performance analysis. Evaluation = "automated verifiable tests" plus a lot of trying the model by hand.
- **Consistency comes from reference images, not fine-tuning.** Gen-4 References take 1–3 reference images for consistent characters and locations
  "without the need for fine-tuning or additional training". https://runway.com/research/introducing-runway-gen-4
- **Fine-tuning is kept for studio-scale deals**, e.g. Lionsgate (a custom model trained on 20k+ titles).
  https://venturebeat.com/ai/runways-gen-4-ai-solves-the-character-consistency-challenge-making-ai-filmmaking-actually-useful

### HeyGen
- **Brand context is passed by ID, never pasted into the prompt.** The Video Agent API takes `brand_kit_id` and `brand_glossary_id`, which point to records saved
  in the workspace. "Neither field accepts inline configuration."
  - The kit "applies your colors, fonts, and logo to every scene the agent composes".
  - The glossary sets pronunciation.
  - A separate `style_id` "picks the look — scene layout, pacing, aesthetic".
  - https://developers.heygen.com/docs/on-brand
- **The glossary is a table of term rules** (CSV bulk upload). https://help.heygen.com/en/articles/8830251-how-to-use-brand-glossary
- **The agent works plan-first.** It shows a video plan, the user approves, then it builds scene by scene, choosing a media type per scene.
  https://help.heygen.com/en/articles/13566094-video-agent-prompting-guide
- **Scenes are composed in code** ("Hyperframes", HTML-to-video), not from fixed templates. (snippet)

### Higgsfield
- **Presets replace prompts.** Founder Alex Mashrabov: for brand advertisers, "avoiding unwanted details makes prompts longer and more
  difficult", so presets / "click-to-video". https://www.antoinebuteau.com/lessons-from-alex-mashrabov/
- **They position themselves as an orchestration layer.** "We orchestrate the entire workflow"; "post-training, fine-tuning, and auto-prompting,
  auto-selection of model for specific use cases"; aim to become "the experts for every new model".
  https://sacra.com/research/alex-mashrabov-higgsfield-ai-video-production/
- **Marketing Studio is template-first.**
  - 1,500+ templates.
  - A product URL is crawled and brand signals fill the template.
  - Each template is tied to a fixed model.
  - Free prompting is only the fallback.
  - https://higgsfield.ai/blog/new-marketing-studio-higgsfield
- **Ad formats and hooks are named options:** 9 ad presets and 25+ hooks. (snippet)
- **Camera moves are presets too:** 100+ named moves in Cinema Studio, applied the same way on every underlying model. (snippet)
- **Soul ID is a small per-identity model.** Training on 20+ photos takes about 3–5 minutes and yields an internal model of the face, combined with 50+
  style presets. https://higgsfield.ai/blog/sould-id-best-character-consistency

### Adobe (Firefly / GenStudio)
- **Custom Models are trained per brand on style or subject** (Henkel, Accenture), with an API for batch production. Self-serve training uses 10–30 images;
  Firefly Foundry covers full brand catalogues.
  https://news.adobe.com/news/2025/03/adobe-firefly-services-custom-models-unlock-on-brand-content-production
- **Brand validation is a separate scoring step.** Guidelines fall into three groups (Brand / Platform / Accessibility); each rule gets
  Pass/Fail, and compliance = passed ÷ tested.
  https://experienceleague.adobe.com/en/docs/genstudio-for-performance-marketing/user-guide/guidelines/brand-validation
- **The judge is an outside LLM:** GenStudio sends copy plus the brand guidelines to Azure OpenAI. (snippet, security fact sheet)

### Typeface (Arc Graph)
- **Uploaded guidelines are turned into rules and filed by channel.** Typeface "automatically reads everything, extracts the rules … categorizes them, and maps them to the
  right channels".
  - At generation time only the matching rules are pulled.
  - A Brand Agent checks outputs.
  - The system surfaces "frequently broken brand guidelines".
  - https://www.typeface.ai/blog/arc-graph-your-brands-brain-that-keeps-your-marketing-consistent-at-scale
- **Learnings pass a human gate before becoming knowledge.** Arc Loop takes performance data; each insight "shows its work", goes through **human review**, then
  becomes reusable knowledge. https://www.typeface.ai/blog/typeface-orchestration-engine

### Jasper (Jasper IQ)
- **Context is split into typed layers:** Brand IQ, Marketing IQ (best practices), Product IQ (claims, disclaimers) and a Knowledge Base
  (live connectors). Output is checked against brand rules. https://www.jasper.ai/jasper-iq
- **Hard rules and learned voice are separate:** the Style Guide holds hard rules; Brand Voice is learned from writing samples.

### Canva
- **The Brand Kit is structured data applied by the editor**, not described to a model. https://www.canva.com/magic-design/
- **Evaluation criteria are written before the prompt** (Magic Switch).
  - Criteria are scored as Information, Intent, Semantic Order, Tone and Format.
  - Regex evaluators handle objective checks; LLM-judge handles subjective ones.
  - Evals run as regression tests.
  - https://www.zenml.io/llmops-database/systematic-llm-evaluation-framework-for-content-generation

### Synthesia
- **The Brand Kit auto-replaces** colours, fonts, avatars and logos; the system applies it, not the model.
  https://docs.synthesia.io/docs/brand-kits

### Midjourney
- **Style is stored as short codes.** `--sref` codes and `--p` personalization profiles are learned from pairwise rankings or moodboards.
  "--sref is targeted; --p is ambient." (docs, snippet)

### Krea
- **A LoRA carries what prompts can't.** Doodles trained a LoRA because prompting stayed "almost-Doodles"; Krea frames the LoRA as "persistent memory for
  the things a prompt can't easily describe". https://www.krea.ai/blog/from-almost-to-doodles

### Google (Veo, Pomelli, ABCD)
- **Veo rewrites short prompts with an LLM.** It is on by default for Veo 2, adding camera and sound detail. (Vertex docs, snippet)
- **Pomelli builds a brand profile from a website:** a crawl produces a "Business DNA" profile, then campaign ideas, then assets.
  https://blog.google/innovation-and-ai/models-and-research/google-labs/pomelli/
- **The ABCDs Detector turns the ABCD framework into per-feature checks** (open source).
  - Each feature is one entry in `features_repository.py`, checked by annotation (Video Intelligence API), by LLM, or both.
  - Checks can run grouped or one at a time.
  - Output per feature: `detected`, `confidence_score`, `detected_evidence` (timestamps), `recommended_actions`.
  - The README warns that human QA is still needed.
  - https://github.com/google-marketing-solutions/abcds-detector

### Meta (Advantage+ / AdLlama)
- **Generation varies the advertiser's existing assets** rather than starting from scratch.
- **AdLlama trains the ad-text model on real performance.** Llama-2-7B was post-trained with **RL from performance feedback** (a CTR reward model): +6.7% CTR
  (p=0.03), across about 35k advertisers and 640k variations. https://arxiv.org/abs/2507.21983

### TikTok Symphony
- **The agent runs a fixed sequence of stages:** product brief → insight report → storyboard → video.
  - It draws on top-performing ads and trends.
  - Users can edit at every stage and get 3 variations.
  - https://ads.tiktok.com/business/en/blog/symphony-agent

### Pencil, AdCreative.ai, Omneky
- **Pencil:** a different model per task, predictive scoring before spend, and performance data flowing back.
  https://trypencil.com/the-platform
- **AdCreative.ai:** component detection plus saliency scoring; each suggestion carries an estimated score gain.
  https://www.adcreative.ai/creative-scoring
- **Omneky:** a brand rules engine, plus predicted CTR for every variation. (snippet)

### Invideo, Luma, Pika, Photoroom
- **Invideo:**
  - A producer agent holds the script and the vision.
  - Specialist sub-agents work "on isolated project pages to prevent feedback contamination" against locked character sheets.
  - Each shot is routed to a chosen model.
  - Human approval gates come before spend.
  - https://invideo.io/faq/how-do-you-set-up-a-multi-agent-ai-video-production/
- **Luma** separates Brainstorm (plan, no render) from Create. https://lumalabs.ai/learning-hub/the-luma-agent-explained
- **Pika** exposes effects and scenes as presets (Pikaffects, Pikascenes "ingredients").
- **Photoroom** expands prompts by default (`expandPrompt.mode: ai.never` turns it off) and supports reference-image guidance.
  https://docs.photoroom.com/image-editing-api-plus-plan/ai-backgrounds

### Research on prompt rewriters
- **DALL-E 3** rewrote every prompt with GPT-4 into a descriptive caption to match its training captions.
- **PromptEnhancer (Tencent Hunyuan, 2025)** trains a chain-of-thought rewriter with RL against "AlignEvaluator", a reward model scoring outputs on
  **24 failure points**. The generator stays unchanged. https://arxiv.org/abs/2509.04545

---

## Part 2 — Common architecture patterns

**(a) Nobody puts all their knowledge in one prompt.** Knowledge travels by different routes:
1. **Structured records referenced by ID.** Brand kits and glossaries are applied by the system, not described to the model.
2. **Rules filed by channel or task and selected per job** (Typeface, Jasper).
3. **Rules as checks after generation, not instructions before it** (Adobe, Typeface, Google ABCD, Canva).
4. **Retrieval for facts only**, never for "how to make a good ad".
5. **Staged pipelines with isolated context per stage** (TikTok, HeyGen, Luma, Invideo).
6. **Model-specific prompt craft lives in a hidden per-model rewriter**, never in the orchestrator (Runway, Veo, Photoroom, DALL-E 3).

**(b) Presets are compiled knowledge.** A preset is model choice, prompt skeleton, negatives, camera and parameters, tested ahead of time.
At run time the agent picks a name and fills slots.

**(c) The mechanism depends on the kind of knowledge:**

| Knowledge type | Mechanism | Examples |
|---|---|---|
| Hard brand identifiers | Structured record applied by the system | HeyGen, Synthesia, Canva |
| One-off look or character | Reference-image conditioning | Runway References, `--sref`, Photoroom |
| Recurring identity or strict style | Small per-customer LoRA (minutes, 3–30 images) | Soul ID, Krea, Firefly Custom |
| Whole catalogue | Custom model | Firefly Foundry, Runway × Lionsgate |
| Facts | Retrieval / connectors | Jasper, Typeface, Pomelli |
| Model prompt craft | Rewriter (sometimes RL-trained) | Runway, Veo, DALL-E 3, PromptEnhancer |
| "What performs" | Scoring models + performance feedback | AdLlama, AdCreative, Pencil, Omneky |

**(d) Small specialised models surround the big generator:** rewriters, judges (per-rule pass/fail with evidence),
detectors and predictors, routers, and learning loops (RLPF, pairwise ranking, human-gated insight promotion).

## Part 3 — What a small team with a big Canon should copy [Inference]

1. **Tag every Canon item by the job it does:** `deterministic_spec`, `preset_ingredient`, `model_prompt_craft`, `check`, `fact`,
   `strategic_heuristic`. Only the last type ever reaches the orchestrator.
2. **Compile the Canon into recipes:** model, params, slot template, negatives, refs, checks and failure modes. Version them and regression-test them.
3. **Give each model its own rewriter:** the orchestrator writes intent; a per-model rewriter card holds that model's craft.
4. **Build a check registry in the ABCD-detector shape:** id, applicability, method, pass criteria, evidence, action.
5. **Keep brand state as typed records referenced by ID.**
6. **Escalate style fidelity step by step:** references first, then a LoRA when the look keeps landing "almost right".
7. **Gate learnings as proposed edits** to a specific recipe, rewriter card or check, with evidence, merged only after review. Track the most-broken rules.
8. **Stage the pipeline and isolate context per stage.**

**Bottom line:** the industry doesn't solve "too much context" with bigger prompts. It splits knowledge into data the
system applies itself, tested recipes, per-model rewriters, small adapters, fact retrieval, and checks after generation.
The LLM chooses and routes; it does not remember everything.
