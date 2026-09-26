# Why a Canon-enriched prompt pipeline loses to the customer's direct prompt

Research appendix 05 of `CONTEXT-SOLUTION.md`. Compiled 2026-09-25. **[secondary]** means the official page blocked our fetch and
the claim rests on search-engine extracts of it. **[recall]** means we did not re-verify it. **[inference]** means it is our reasoning.
No public enhancer-on/off A/B numbers were found from fal, Krea, Freepik, Leonardo, Canva, Adobe, HeyGen or Higgsfield.

---

## A. Prompt length, structure and text encoders

1. **FLUX.1 (diffusers docs)** https://huggingface.co/docs/diffusers/main/en/api/pipelines/flux
   - The CLIP encoder is hard-truncated at **77 tokens**. T5 takes 512 by default (256 on schnell).
   - The pooled CLIP vector, which carries global style and subject, sees only the first 77 tokens.
2. **SD3/3.5 (diffusers docs)** https://huggingface.co/docs/diffusers/main/en/api/pipelines/stable_diffusion/stable_diffusion_3
   - T5 takes 256 tokens by default. Anything longer is silently truncated.
3. **Long-CLIP** https://arxiv.org/abs/2403.15378
   - CLIP's "actual effective length is even less than 20" tokens.
4. **DetailMaster** https://arxiv.org/html/2505.16915v1
   - Long prompts average about 285 tokens. **All** models degrade as prompts grow, including SDXL, SD3.5, FLUX.1, Gemini 2.0 Flash and GPT-Image-1. The decline is clear past about 250 tokens.
   - Character attributes and locations reach only about 50% accuracy.
   - Named mechanisms: training captions of 10–20 tokens, and "detail overload causing attribute omission/distortion".
5. **GenEval 2** https://arxiv.org/html/2512.16853
   - Whole-prompt accuracy falls from about **58% with 3 atoms to about 4% with 10 atoms**. The best model scores 85.3% per atom but only 35.8% per prompt.
   - Automated judges drift on newer models.
   - **Every extra constraint multiplies the chance of failure.**
6. **T2I-CompBench++** https://arxiv.org/html/2307.06350
   - GPT-4 detailed rephrasing (8 words → 24 words) did not help attribute binding on SDXL: 0.5879 before, 0.5781 after.
7. **Black Forest Labs, FLUX.2 guide** https://docs.bfl.ai/guides/prompting_guide_flux2
   - **30–80 words is ideal.** "Word order matters – FLUX.2 pays more attention to what comes first."
   - Structure: Subject + Action + Style + Context.
   - **No negative prompts**: describe the positive state instead.
   - JSON prompts are supported.
8. **Google Imagen guide** https://docs.cloud.google.com/vertex-ai/generative-ai/docs/image/img-gen-prompt-guide
   - "Don't require excessive length".
   - In-image text: 25 characters or fewer, and 2–3 phrases at most.
9. **Gemini 2.5 Flash Image guide** https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/
   - Describe the scene and state its purpose.
   - **Semantic negatives** ("an empty street", not "no cars").
   - For edits, say "keep everything else the same".
10. **OpenAI gpt-image-1.5 guide** https://developers.openai.com/cookbook/examples/multimodal/image-gen-1.5-prompting_guide
    - State the intended use.
    - "Start with a clean base prompt, then refine with small, single-change follow-ups."
    - The tool rewrites prompts itself (`revised_prompt`).
11. **Veo 3.1 guide** https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
    - Formula: Cinematography + Subject + Action + Context + Style. Examples run 2–4 sentences.
    - Reference images ("ingredients"), first/last frame.
12. **Veo prompt rewriter** [secondary] https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/turn-the-prompt-rewriter-off
    - The LLM rewriter "can't be disabled" for Veo 3 / 3.1.
    - **Our prompt is rewritten a second time.**
13. **Runway image-to-video guide** [secondary] https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide
    - "Focus almost exclusively on motion."
    - "Reiterating elements that exist within the image in high detail can lead to **reduced motion or unexpected results**."
14. **Kling** [secondary] / fal's Kling 3.0 guide https://blog.fal.ai/kling-3-0-prompting-guide/
    - For image-to-video, drop what the image already shows and lead with movement and camera.
15. **Midjourney** [secondary]
    - "Short and simple prompts typically generate the best images"; avoid "long lists or detailed instructions".
16. **Ideogram**
    - Magic Prompt "Auto" decides by prompt length whether to expand.
    - Ideogram 4 was trained on ordered JSON captions, so plain-text prompts "will not work". **The prompt must match the training-caption format.**
    - https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md
17. **Qwen-Image** https://github.com/QwenLM/Qwen-Image
    - The vendor rewriter is "strongly recommend[ed]".
18. **Seedream** https://fal.ai/learn/devs/seedream-v4-5-prompt-guide
    - Avoid "overloading prompts with mixed styles or too many adjectives".
19. **fal Wan `enable_prompt_expansion`**
    - Defaults differ by endpoint. Audit each one.

## B. Prompt rewriting and expansion research

20. **DALL·E 3** https://cdn.openai.com/papers/dall-e-3.pdf
    - Trained on 95% synthetic descriptive captions.
    - Upsampling works when its output **resembles the training captions**: plain, literal, visual.
21. **Google Prompt Expansion** https://arxiv.org/html/2312.16720
    - Only slight aesthetic wins (0.52 or better), gained through diversity.
    - Alignment was about 70% "equivalent". Expansion "can never be expected to increase the degree of alignment".
    - Specific queries benefit least, and details can get dropped.
22. **Promptist (Microsoft)** https://arxiv.org/abs/2212.09611
    - Rewriting helps when trained with RL against a measured reward that preserves intent.
23. **OPT2I (Meta)** https://arxiv.org/abs/2403.17804
    - DSG +12–25%.
    - The winning edits **move ignored elements to the front** or elaborate only the missing ones.
24. **FaithRewriter, "Seeing is Believing"** (Jun 2026) https://arxiv.org/html/2606.08492v1
    - VQA score: raw prompt **62.12**, text-only LLM rewrite **59.12**, visually grounded rewriter 63.27.
    - **The LLM rewrite scores lower than the raw prompt.** Text-only rewriters "hallucinate details that sound linguistically reasonable but are visually or physically impossible".
    - A good rewriter leaves an already-specific prompt unchanged.
25. **PromptEnhancer (Tencent)** https://arxiv.org/html/2509.04545v5
    - +5.1% on average, trained against a reward.
    - Regresses on **text layout (−0.7%)**. The authors warn of over-specification.
26. **RePrompt (Microsoft)** https://arxiv.org/abs/2505.17540
    - Plain LLM enhancers "frequently generate stylistic or unrealistic content". RL against image rewards fixes this.
27. **Reward-trained rewriters transfer across models** https://arxiv.org/abs/2510.12041
28. **"A Creative Agent is Worth a 64-Token Template"** https://arxiv.org/abs/2603.17895
    - A learned fixed template matched or beat a per-request creative agent, **3.7× faster and 4.8× cheaper**.

## C. Selection, verification and inference-time compute

29. **Inference-time scaling for diffusion (Google 2025)** https://arxiv.org/html/2501.09732
    - Seed search with a verifier: FLUX.1-dev ImageReward went from 0.97 to 1.58.
    - A smaller model with search beat FLUX without search.
    - Watch for verifier hacking. Use an ensemble.
30. **PickScore** https://arxiv.org/html/2305.01569
    - Predicts human preference 70.5% of the time, against 68.0% for human experts.
    - Picking the best image with it beats random picking 71.4% of the time.
31. **HPSv3** https://arxiv.org/abs/2508.03789
    - 76.9% accuracy on HPDv3.
32. **ImageReward** https://arxiv.org/abs/2304.05977
33. **VQAScore / GenAI-Bench** https://arxiv.org/abs/2404.01291
    - The probability of "Yes" to "does this show {text}?". Beats CLIPScore and GPT-4V metrics. Works for video.
34. **DSG, Davidsonian Scene Graph** https://arxiv.org/abs/2310.18235
    - Turns a prompt into atomic, dependency-ordered yes/no questions. **This is the right format for a verifiable brief checklist.**
35. **VIEScore** https://arxiv.org/abs/2312.14867
    - A GPT-4o judge scores Spearman 0.4 against humans; human-to-human agreement is 0.45.
36. **GenAI-Arena** https://arxiv.org/abs/2406.04485
    - The best VLM reproduces human pairwise preference **only 49% of the time**. Holistic "which is better?" judging is unreliable. Use atomic checks and calibrate on your own verdicts.
37. **Bandit routing across models**
    - PAK-UCB https://arxiv.org/html/2410.13287v4
    - PromptWise (cost-aware) https://arxiv.org/pdf/2505.18901
    - DAK-UCB https://arxiv.org/abs/2603.23140

## D. Practitioner and vendor evidence

- Every major vendor ships **its own rewriter** tuned to its caption distribution. It is applied mainly to **short** prompts: Ideogram decides by prompt length, and Veo returns its rewrite only when the prompt was under 30 words.
- Pencil's performance score is validated on 7,000+ ads (vendor-reported). Ad knowledge is used there to **score and rank**, not to write prompts.

---

## Part 2: Why the Canon-enriched pipeline underperforms

In order of likelihood and strength of evidence:

1. **Constraint count multiplies failure.** GenEval 2: about 58% at 3 atoms, about 4% at 10 atoms. The customer's prompt has 2–4 atoms.
2. **The prompt doesn't match the training-caption distribution.** Canon vocabulary is strategy, not visual description. FaithRewriter's LLM rewrite scored **below the raw prompt**.
3. **Truncation and position.** CLIP has 77 tokens and an effective length under 20. T5 truncates silently. FLUX weights the first tokens.
4. **Double rewriting.** Veo 3, OpenAI and Qwen rewrite our already-expanded prompt again. **[inference]**
5. **Over-specification overrides the model's own taste.** In image-to-video it also kills motion (Runway).
6. **Hallucinated or unrequested details** get judged as "not what I asked".
7. **Text overload** in-image. Typography regresses even with reward-trained rewriters.
8. **No ablation**, so every global prompt edit changes many atoms at once. That is why "every fix breaks something else".

## Part 3: Evidence-backed architecture

1. **Keep the Canon out of the generation prompt.** Use it to **plan** (what the ad needs) and to **judge** (DSG-style atomic questions).
2. **A structured IR with a controlled vocabulary**:
   - keep `intent_verbatim`;
   - enumerated framing, lighting and style values, each mapped to phrasing tested on that model;
   - a **must_have cap of 4–6 atoms**;
   - everything else goes to the judge or to compositing.
3. **A per-model prompt compiler** renders only the slots that model responds to:
   - FLUX.2, Seedream, Imagen: 30–80 words, subject-first, positive phrasing;
   - Ideogram 4: JSON;
   - gpt-image and Gemini: a narrative plus the intended use;
   - Veo: short and literal, because it will be rewritten again;
   - image-to-video: **motion and camera only**.
   Keep each adapter as a small versioned template with golden tests. Don't stack our rewriter on top of the vendor's.
4. **References, edits and compositing over text.**
5. **Best-of-N with layered verifiers**:
   - hard filter: DSG atomic checks;
   - rank: HPSv3 or PickScore;
   - tiebreak: a pairwise VLM.
   Calibrate every judge on our own accept/reject verdicts. At p=0.3 per sample, N=4 gives 76% ≥1 acceptable.
6. **Rewrite only when a measurement says it helps.** Pass concrete requests through unchanged. Lightly expand vague ones. Use OPT2I-style targeted deltas on failed atoms.
7. **Ablate every piece of knowledge and keep the direct-prompt arm forever.**
   - Arms: direct / compiled slots / compiled + rule X, run as paired comparisons.
   - A rule enters the prompt only if it wins about 100 or more stratified pairs.
   - A bandit routes across (model × strategy) with reward = acceptance − λ·cost, with a 5–10% floor on the direct arm.
   - A golden regression set of 100–300 requests.
8. **Later, learn it:** distil winning prompts into per-model templates, or train a small reward-optimised rewriter.
