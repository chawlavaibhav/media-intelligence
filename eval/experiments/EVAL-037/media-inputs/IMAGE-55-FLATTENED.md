# EVAL-037 — IMAGE-55 FLATTENED GENERATION INPUT

**Use this one file only.** Do not browse GitHub, inspect branches, fetch EVAL-037 reasoning files, or regenerate reasoning.

This file will contain all **55 eligible image generation plans**.

## Stability / laptop-safe execution
- Process **one image job at a time**.
- Keep only one active generation at once.
- Do not load or reason over all 55 cards simultaneously.
- Read the next card, generate it, persist/checkpoint the result, then continue.
- If interrupted, resume from the first unfinished job.
- Exactly one first-pass generation per job.
- One bounded repair only for an objective hard failure.
- Maximum 2 generation attempts per job.
- Never retry just because another style might be nicer.

Objective hard failure = wrong medium/aspect ratio, missing mandatory exact element, unusably malformed output, or direct hard-constraint violation.

For each job record: job id; source key; attempt count; final status (image_complete_first_pass / image_complete_repaired / image_failed); repair reason if any; exact generation prompt sent; final output reference/path.

Use the included execution card as authority. Do not re-research or creatively rewrite it before generation.

## Frozen customer briefs

### B02
I am aight. Create one premium promotional poster for our media-generation API for Indian businesses during the festive season. The key commercial proposition is: image generation at ₹9 and video generation at ₹99. Both prices must be immediately understandable, but the design must still feel like a serious AI infrastructure/product company rather than a discount retail flyer. Make typography and information hierarchy do most of the work. You may use only aight's official website, https://getaight.ai, for product and brand information. Deliverable: one 4:5 poster.

### B03
Create one premium 4:5 advertising image for a new Indian sparkling drink made from mosambi and sparkling water. It is aimed at urban consumers aged roughly 22–35. The product should feel refreshing, sophisticated and culturally contemporary while still retaining the familiarity of mosambi. Avoid clichéd "Indian" visual shorthand and avoid making it look like a cheap soft drink. The product must be the unmistakable hero. No celebrity and no external website.

### B06
Create one premium 4:5 e-commerce hero image for a fictional mechanical watch called the Aster Meridian 38. Product facts are fixed: 38 mm brushed stainless-steel case, deep blue sunburst dial, silver baton hour markers, silver dauphine hands, no date window, domed sapphire crystal and a dark brown leather strap. The image must communicate craftsmanship, dial detail, material quality and wrist-watch desirability while remaining commercially useful on a premium product page. Product geometry and details must not be casually altered. Avoid generic floating-product CGI unless the creative idea genuinely requires it. No external website.

---

# IMAGE JOB I01 — B02

Source key: E037-haiku-no-canon-B02-R1
Use frozen brief B02 from the top of this file.

## DELIVERABLE
One vertical premium promotional poster (4:5 aspect ratio / 1000×1250px recommended) for aight's media-generation API, positioned for Indian businesses during festive season, highlighting ₹9 image and ₹99 video pricing.

---

### OBJECTIVE_INTERPRETATION
Convert aight's core positioning—"Where Indian businesses buy AI"—into a visual pitch that makes pricing transparent and compelling while reinforcing the brand's infrastructure-quality, founder-led, India-first identity. The festive season context allows celebration of accessibility, but the design must signal serious capability and fiscal responsibility (aight's "hard caps," "spend you can see").

---

### CORE_CREATIVE_IDEA
**Typographic clarity as product credibility.** Present pricing and value through deliberate information hierarchy and precise typography—no discount-aesthetic imagery. The poster's structure itself demonstrates the cost-control and transparency aight promises. Minimal color, maximum legibility. The design says: "We're not a discount service; we're infrastructure that happens to cost less because we're built for India."

---

### MESSAGE_AND_INFORMATION_HIERARCHY

1. **Primary headline (dominate space):** ₹9 per image · ₹99 per video  
   *(typography scale/weight establishes price as the power statement)*

2. **Secondary headline (brand + permission):** Aight · Prepaid AI for Indian businesses  
   *(reintroduces brand identity and pillars)*

3. **Tertiary messaging (value proof):** Set hard caps. Track live. One GST invoice.  
   *(supports the "billed right" credibility pillar)*

4. **Festive context (accent line):** Build faster this season.  
   *(timely, minimal, not dominant)*

5. **Call-to-action (foot of poster):** getaight.ai  
   *(simple domain, no slack/urgency language)*

---

### VISUAL_SYSTEM

**Color palette:**
- **Primary:** Deep matte black background (confidence, infrastructure, India-first institutional feel)
- **Type accent:** Crisp white (₹9 and ₹99 figures) and a single secondary color—deep saffron or electric indigo (₹ symbol, thin accent line)—to signal India and modernity without cliché

**Typography:**
- **Headline figures (₹9 / ₹99):** Bold, geometric sans-serif (e.g., Inter Bold, Rigth Grotesk, or similar), sized 180–220px to dominate viewport
- **Body/supporting text:** Lighter weight of same family or neutral sans-serif (e.g., Inter Regular); 18–24px
- **Hierarchy maintained through scale and weight, not color noise**

**Layout structure:**
- Vertical flow: logo/brand mark at top (small, 40–60px)
- Central zone (60–75% of poster): ₹9 and ₹99 positioned left-right or stacked with clear visual separation (thin horizontal line)
- Below pricing: short supporting line ("Image generation · Video generation" or minimal label)
- Mid-poster: one sentence of proof ("Set hard caps. Track live. One GST invoice.")
- Footer (10% of space): small "Aight · getaight.ai"
- Festive note ("Build faster this season") tucked as a thin accent line in one corner or baseline

**Whitespace:** Generous. Allows each element to breathe and signals premium/confidence.

---

### PRODUCTION_RECIPE

1. **Grid structure:** 1000×1250px at 300dpi (poster-quality print)
2. **Base layer:** Black background (#000000 or slight warm-black)
3. **Typesetting passes:**
   - Position and style ₹9 and ₹99 as anchor elements (white, bold, 200px+)
   - Add currency symbol in saffron/indigo accent color (₹)
   - Layer supporting text in hierarchy
   - Apply subtle letter-spacing and line-height to reinforce premium feel
4. **Accent line:** Thin horizontal or vertical rule in saffron/indigo, separating price figures or framing core message
5. **Fine-tuning:** Kerning, baseline alignment, optical spacing for a hand-refined feel (not automatic)
6. **Final pass:** Confirm all text meets festive context without aesthetic violation (no icons, no gradients, no photography)

---

### GENERATION_PROMPTS

**Single master construction prompt:**

> Create a premium vertical poster (4:5, 1000×1250px) for aight, an Indian AI API platform. Design is typographic-led, black background. Center the price figures ₹9 (image generation) and ₹99 (video generation) in bold geometric sans-serif white type (180–220px). Surround with supporting text in white/gray: "Aight · Prepaid AI for Indian businesses" top; "Set hard caps. Track live. One GST invoice." as subhead; "getaight.ai" footer. Use one saffron or electric indigo accent color for the ₹ symbols and a single thin rule. Include small festive marker: "Build faster this season" as an accent. No photography, icons, or illustrations. Lettering and spacing alone convey premium infrastructure credibility, not retail discount. Poster is suitable for print and digital festive promotion to Indian business audiences.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- Typographic treatment (manual kerning, optical spacing, leading) should be refined post-generation
- Currency symbols (₹) must be precisely placed and color-correct
- Aight brand mark/wordmark placement must align with official brand identity
- Text strings are fixed (no variation):
  - ₹9 / ₹99
  - "Aight · Prepaid AI for Indian businesses"
  - "Set hard caps. Track live. One GST invoice."
  - "getaight.ai"
  - "Build faster this season"

**Design approval gating:**
- Confirm festive tone is subtle, not visually dominant (should not cheapen the brand)
- Verify pricing figures are the dominant visual anchor
- Check that black background and minimal color scheme feel premium, not austere

---

### AUDIO_AND_EDIT

N/A (static image deliverable).

---

### FAILURE_PREVENTION

1. **Price visibility failing:** If ₹9 and ₹99 are not immediately scannable (first 1 second), redesign scale/positioning. Test with rapid eye-track.
2. **Brand confusion:** If the design feels like a retail sale flyer rather than infrastructure product, increase whitespace, reduce festive ornamentation, enforce sober typography.
3. **Readability in digital/small sizes:** Test poster at 500×625px thumbnail; if text collapses, increase font size or adjust hierarchy.
4. **Localization misstep:** Confirm ₹ symbol and Hinglish/English language balance match aight's existing materials (site uses English; this poster should too, with India-first context clear through rupee currency and brand statement).
5. **Color contrast:** Ensure saffron/indigo accent does not create visual noise or reduce premium feel; test against black background for legibility and sophistication.

---

### HARD_CONSTRAINT_CHECK

✅ **4:5 aspect ratio:** Poster dimensions specified and applied  
✅ **Pricing visibility:** ₹9 and ₹99 positioned as primary visual hierarchy  
✅ **Premium tone:** Typography-led, no retail aesthetic, infrastructure credibility maintained  
✅ **Festive season context:** Incorporated as subtle accent ("Build faster this season"), not dominant  
✅ **Indian business target:** Rupee currency, aight's prepaid/GST/founder-support messaging, "hard caps" proof point included  
✅ **Single concept:** One poster design, no alternatives  
✅ **aight brand/product info sourced from official website only:** All messaging grounded in getaight.ai content (prepaid wallet, hard caps, GST, cost control, "Where Indian businesses buy AI")  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (frozen snapshot)
  - Brand positioning: "Where Indian businesses buy AI"
  - Core pillars: prepaid rupee wallet, hard caps, one domestic GST invoice, founder support
  - Product offerings: text (GPT, Claude, Gemini), voice (Sarvam, Smallest, ElevenLabs), image (curated set)
  - Key differentiators: cost control ("Spend you can see"), transparency, India-first infrastructure, minimal onboarding
  - Target customer profile: Indian teams, production AI workflows, cost-conscious enterprises

**No external sources or assumptions were applied beyond the aight website.**

---

## OBJECTIVE_INTERPRETATION
Convert aight's core positioning—"Where Indian businesses buy AI"—into a visual pitch that makes pricing transparent and compelling while reinforcing the brand's infrastructure-quality, founder-led, India-first identity. The festive season context allows celebration of accessibility, but the design must signal serious capability and fiscal responsibility (aight's "hard caps," "spend you can see").

---

### CORE_CREATIVE_IDEA
**Typographic clarity as product credibility.** Present pricing and value through deliberate information hierarchy and precise typography—no discount-aesthetic imagery. The poster's structure itself demonstrates the cost-control and transparency aight promises. Minimal color, maximum legibility. The design says: "We're not a discount service; we're infrastructure that happens to cost less because we're built for India."

---

### MESSAGE_AND_INFORMATION_HIERARCHY

1. **Primary headline (dominate space):** ₹9 per image · ₹99 per video  
   *(typography scale/weight establishes price as the power statement)*

2. **Secondary headline (brand + permission):** Aight · Prepaid AI for Indian businesses  
   *(reintroduces brand identity and pillars)*

3. **Tertiary messaging (value proof):** Set hard caps. Track live. One GST invoice.  
   *(supports the "billed right" credibility pillar)*

4. **Festive context (accent line):** Build faster this season.  
   *(timely, minimal, not dominant)*

5. **Call-to-action (foot of poster):** getaight.ai  
   *(simple domain, no slack/urgency language)*

---

### VISUAL_SYSTEM

**Color palette:**
- **Primary:** Deep matte black background (confidence, infrastructure, India-first institutional feel)
- **Type accent:** Crisp white (₹9 and ₹99 figures) and a single secondary color—deep saffron or electric indigo (₹ symbol, thin accent line)—to signal India and modernity without cliché

**Typography:**
- **Headline figures (₹9 / ₹99):** Bold, geometric sans-serif (e.g., Inter Bold, Rigth Grotesk, or similar), sized 180–220px to dominate viewport
- **Body/supporting text:** Lighter weight of same family or neutral sans-serif (e.g., Inter Regular); 18–24px
- **Hierarchy maintained through scale and weight, not color noise**

**Layout structure:**
- Vertical flow: logo/brand mark at top (small, 40–60px)
- Central zone (60–75% of poster): ₹9 and ₹99 positioned left-right or stacked with clear visual separation (thin horizontal line)
- Below pricing: short supporting line ("Image generation · Video generation" or minimal label)
- Mid-poster: one sentence of proof ("Set hard caps. Track live. One GST invoice.")
- Footer (10% of space): small "Aight · getaight.ai"
- Festive note ("Build faster this season") tucked as a thin accent line in one corner or baseline

**Whitespace:** Generous. Allows each element to breathe and signals premium/confidence.

---

### PRODUCTION_RECIPE

1. **Grid structure:** 1000×1250px at 300dpi (poster-quality print)
2. **Base layer:** Black background (#000000 or slight warm-black)
3. **Typesetting passes:**
   - Position and style ₹9 and ₹99 as anchor elements (white, bold, 200px+)
   - Add currency symbol in saffron/indigo accent color (₹)
   - Layer supporting text in hierarchy
   - Apply subtle letter-spacing and line-height to reinforce premium feel
4. **Accent line:** Thin horizontal or vertical rule in saffron/indigo, separating price figures or framing core message
5. **Fine-tuning:** Kerning, baseline alignment, optical spacing for a hand-refined feel (not automatic)
6. **Final pass:** Confirm all text meets festive context without aesthetic violation (no icons, no gradients, no photography)

---

### GENERATION_PROMPTS

**Single master construction prompt:**

> Create a premium vertical poster (4:5, 1000×1250px) for aight, an Indian AI API platform. Design is typographic-led, black background. Center the price figures ₹9 (image generation) and ₹99 (video generation) in bold geometric sans-serif white type (180–220px). Surround with supporting text in white/gray: "Aight · Prepaid AI for Indian businesses" top; "Set hard caps. Track live. One GST invoice." as subhead; "getaight.ai" footer. Use one saffron or electric indigo accent color for the ₹ symbols and a single thin rule. Include small festive marker: "Build faster this season" as an accent. No photography, icons, or illustrations. Lettering and spacing alone convey premium infrastructure credibility, not retail discount. Poster is suitable for print and digital festive promotion to Indian business audiences.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- Typographic treatment (manual kerning, optical spacing, leading) should be refined post-generation
- Currency symbols (₹) must be precisely placed and color-correct
- Aight brand mark/wordmark placement must align with official brand identity
- Text strings are fixed (no variation):
  - ₹9 / ₹99
  - "Aight · Prepaid AI for Indian businesses"
  - "Set hard caps. Track live. One GST invoice."
  - "getaight.ai"
  - "Build faster this season"

**Design approval gating:**
- Confirm festive tone is subtle, not visually dominant (should not cheapen the brand)
- Verify pricing figures are the dominant visual anchor
- Check that black background and minimal color scheme feel premium, not austere

---

### AUDIO_AND_EDIT

N/A (static image deliverable).

---

### FAILURE_PREVENTION

1. **Price visibility failing:** If ₹9 and ₹99 are not immediately scannable (first 1 second), redesign scale/positioning. Test with rapid eye-track.
2. **Brand confusion:** If the design feels like a retail sale flyer rather than infrastructure product, increase whitespace, reduce festive ornamentation, enforce sober typography.
3. **Readability in digital/small sizes:** Test poster at 500×625px thumbnail; if text collapses, increase font size or adjust hierarchy.
4. **Localization misstep:** Confirm ₹ symbol and Hinglish/English language balance match aight's existing materials (site uses English; this poster should too, with India-first context clear through rupee currency and brand statement).
5. **Color contrast:** Ensure saffron/indigo accent does not create visual noise or reduce premium feel; test against black background for legibility and sophistication.

---

### HARD_CONSTRAINT_CHECK

✅ **4:5 aspect ratio:** Poster dimensions specified and applied  
✅ **Pricing visibility:** ₹9 and ₹99 positioned as primary visual hierarchy  
✅ **Premium tone:** Typography-led, no retail aesthetic, infrastructure credibility maintained  
✅ **Festive season context:** Incorporated as subtle accent ("Build faster this season"), not dominant  
✅ **Indian business target:** Rupee currency, aight's prepaid/GST/founder-support messaging, "hard caps" proof point included  
✅ **Single concept:** One poster design, no alternatives  
✅ **aight brand/product info sourced from official website only:** All messaging grounded in getaight.ai content (prepaid wallet, hard caps, GST, cost control, "Where Indian businesses buy AI")  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (frozen snapshot)
  - Brand positioning: "Where Indian businesses buy AI"
  - Core pillars: prepaid rupee wallet, hard caps, one domestic GST invoice, founder support
  - Product offerings: text (GPT, Claude, Gemini), voice (Sarvam, Smallest, ElevenLabs), image (curated set)
  - Key differentiators: cost control ("Spend you can see"), transparency, India-first infrastructure, minimal onboarding
  - Target customer profile: Indian teams, production AI workflows, cost-conscious enterprises

**No external sources or assumptions were applied beyond the aight website.**

---

## CORE_CREATIVE_IDEA
**Typographic clarity as product credibility.** Present pricing and value through deliberate information hierarchy and precise typography—no discount-aesthetic imagery. The poster's structure itself demonstrates the cost-control and transparency aight promises. Minimal color, maximum legibility. The design says: "We're not a discount service; we're infrastructure that happens to cost less because we're built for India."

---

### MESSAGE_AND_INFORMATION_HIERARCHY

1. **Primary headline (dominate space):** ₹9 per image · ₹99 per video  
   *(typography scale/weight establishes price as the power statement)*

2. **Secondary headline (brand + permission):** Aight · Prepaid AI for Indian businesses  
   *(reintroduces brand identity and pillars)*

3. **Tertiary messaging (value proof):** Set hard caps. Track live. One GST invoice.  
   *(supports the "billed right" credibility pillar)*

4. **Festive context (accent line):** Build faster this season.  
   *(timely, minimal, not dominant)*

5. **Call-to-action (foot of poster):** getaight.ai  
   *(simple domain, no slack/urgency language)*

---

### VISUAL_SYSTEM

**Color palette:**
- **Primary:** Deep matte black background (confidence, infrastructure, India-first institutional feel)
- **Type accent:** Crisp white (₹9 and ₹99 figures) and a single secondary color—deep saffron or electric indigo (₹ symbol, thin accent line)—to signal India and modernity without cliché

**Typography:**
- **Headline figures (₹9 / ₹99):** Bold, geometric sans-serif (e.g., Inter Bold, Rigth Grotesk, or similar), sized 180–220px to dominate viewport
- **Body/supporting text:** Lighter weight of same family or neutral sans-serif (e.g., Inter Regular); 18–24px
- **Hierarchy maintained through scale and weight, not color noise**

**Layout structure:**
- Vertical flow: logo/brand mark at top (small, 40–60px)
- Central zone (60–75% of poster): ₹9 and ₹99 positioned left-right or stacked with clear visual separation (thin horizontal line)
- Below pricing: short supporting line ("Image generation · Video generation" or minimal label)
- Mid-poster: one sentence of proof ("Set hard caps. Track live. One GST invoice.")
- Footer (10% of space): small "Aight · getaight.ai"
- Festive note ("Build faster this season") tucked as a thin accent line in one corner or baseline

**Whitespace:** Generous. Allows each element to breathe and signals premium/confidence.

---

### PRODUCTION_RECIPE

1. **Grid structure:** 1000×1250px at 300dpi (poster-quality print)
2. **Base layer:** Black background (#000000 or slight warm-black)
3. **Typesetting passes:**
   - Position and style ₹9 and ₹99 as anchor elements (white, bold, 200px+)
   - Add currency symbol in saffron/indigo accent color (₹)
   - Layer supporting text in hierarchy
   - Apply subtle letter-spacing and line-height to reinforce premium feel
4. **Accent line:** Thin horizontal or vertical rule in saffron/indigo, separating price figures or framing core message
5. **Fine-tuning:** Kerning, baseline alignment, optical spacing for a hand-refined feel (not automatic)
6. **Final pass:** Confirm all text meets festive context without aesthetic violation (no icons, no gradients, no photography)

---

### GENERATION_PROMPTS

**Single master construction prompt:**

> Create a premium vertical poster (4:5, 1000×1250px) for aight, an Indian AI API platform. Design is typographic-led, black background. Center the price figures ₹9 (image generation) and ₹99 (video generation) in bold geometric sans-serif white type (180–220px). Surround with supporting text in white/gray: "Aight · Prepaid AI for Indian businesses" top; "Set hard caps. Track live. One GST invoice." as subhead; "getaight.ai" footer. Use one saffron or electric indigo accent color for the ₹ symbols and a single thin rule. Include small festive marker: "Build faster this season" as an accent. No photography, icons, or illustrations. Lettering and spacing alone convey premium infrastructure credibility, not retail discount. Poster is suitable for print and digital festive promotion to Indian business audiences.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- Typographic treatment (manual kerning, optical spacing, leading) should be refined post-generation
- Currency symbols (₹) must be precisely placed and color-correct
- Aight brand mark/wordmark placement must align with official brand identity
- Text strings are fixed (no variation):
  - ₹9 / ₹99
  - "Aight · Prepaid AI for Indian businesses"
  - "Set hard caps. Track live. One GST invoice."
  - "getaight.ai"
  - "Build faster this season"

**Design approval gating:**
- Confirm festive tone is subtle, not visually dominant (should not cheapen the brand)
- Verify pricing figures are the dominant visual anchor
- Check that black background and minimal color scheme feel premium, not austere

---

### AUDIO_AND_EDIT

N/A (static image deliverable).

---

### FAILURE_PREVENTION

1. **Price visibility failing:** If ₹9 and ₹99 are not immediately scannable (first 1 second), redesign scale/positioning. Test with rapid eye-track.
2. **Brand confusion:** If the design feels like a retail sale flyer rather than infrastructure product, increase whitespace, reduce festive ornamentation, enforce sober typography.
3. **Readability in digital/small sizes:** Test poster at 500×625px thumbnail; if text collapses, increase font size or adjust hierarchy.
4. **Localization misstep:** Confirm ₹ symbol and Hinglish/English language balance match aight's existing materials (site uses English; this poster should too, with India-first context clear through rupee currency and brand statement).
5. **Color contrast:** Ensure saffron/indigo accent does not create visual noise or reduce premium feel; test against black background for legibility and sophistication.

---

### HARD_CONSTRAINT_CHECK

✅ **4:5 aspect ratio:** Poster dimensions specified and applied  
✅ **Pricing visibility:** ₹9 and ₹99 positioned as primary visual hierarchy  
✅ **Premium tone:** Typography-led, no retail aesthetic, infrastructure credibility maintained  
✅ **Festive season context:** Incorporated as subtle accent ("Build faster this season"), not dominant  
✅ **Indian business target:** Rupee currency, aight's prepaid/GST/founder-support messaging, "hard caps" proof point included  
✅ **Single concept:** One poster design, no alternatives  
✅ **aight brand/product info sourced from official website only:** All messaging grounded in getaight.ai content (prepaid wallet, hard caps, GST, cost control, "Where Indian businesses buy AI")  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (frozen snapshot)
  - Brand positioning: "Where Indian businesses buy AI"
  - Core pillars: prepaid rupee wallet, hard caps, one domestic GST invoice, founder support
  - Product offerings: text (GPT, Claude, Gemini), voice (Sarvam, Smallest, ElevenLabs), image (curated set)
  - Key differentiators: cost control ("Spend you can see"), transparency, India-first infrastructure, minimal onboarding
  - Target customer profile: Indian teams, production AI workflows, cost-conscious enterprises

**No external sources or assumptions were applied beyond the aight website.**

---

## MESSAGE_AND_INFORMATION_HIERARCHY
1. **Primary headline (dominate space):** ₹9 per image · ₹99 per video  
   *(typography scale/weight establishes price as the power statement)*

2. **Secondary headline (brand + permission):** Aight · Prepaid AI for Indian businesses  
   *(reintroduces brand identity and pillars)*

3. **Tertiary messaging (value proof):** Set hard caps. Track live. One GST invoice.  
   *(supports the "billed right" credibility pillar)*

4. **Festive context (accent line):** Build faster this season.  
   *(timely, minimal, not dominant)*

5. **Call-to-action (foot of poster):** getaight.ai  
   *(simple domain, no slack/urgency language)*

---

### VISUAL_SYSTEM

**Color palette:**
- **Primary:** Deep matte black background (confidence, infrastructure, India-first institutional feel)
- **Type accent:** Crisp white (₹9 and ₹99 figures) and a single secondary color—deep saffron or electric indigo (₹ symbol, thin accent line)—to signal India and modernity without cliché

**Typography:**
- **Headline figures (₹9 / ₹99):** Bold, geometric sans-serif (e.g., Inter Bold, Rigth Grotesk, or similar), sized 180–220px to dominate viewport
- **Body/supporting text:** Lighter weight of same family or neutral sans-serif (e.g., Inter Regular); 18–24px
- **Hierarchy maintained through scale and weight, not color noise**

**Layout structure:**
- Vertical flow: logo/brand mark at top (small, 40–60px)
- Central zone (60–75% of poster): ₹9 and ₹99 positioned left-right or stacked with clear visual separation (thin horizontal line)
- Below pricing: short supporting line ("Image generation · Video generation" or minimal label)
- Mid-poster: one sentence of proof ("Set hard caps. Track live. One GST invoice.")
- Footer (10% of space): small "Aight · getaight.ai"
- Festive note ("Build faster this season") tucked as a thin accent line in one corner or baseline

**Whitespace:** Generous. Allows each element to breathe and signals premium/confidence.

---

### PRODUCTION_RECIPE

1. **Grid structure:** 1000×1250px at 300dpi (poster-quality print)
2. **Base layer:** Black background (#000000 or slight warm-black)
3. **Typesetting passes:**
   - Position and style ₹9 and ₹99 as anchor elements (white, bold, 200px+)
   - Add currency symbol in saffron/indigo accent color (₹)
   - Layer supporting text in hierarchy
   - Apply subtle letter-spacing and line-height to reinforce premium feel
4. **Accent line:** Thin horizontal or vertical rule in saffron/indigo, separating price figures or framing core message
5. **Fine-tuning:** Kerning, baseline alignment, optical spacing for a hand-refined feel (not automatic)
6. **Final pass:** Confirm all text meets festive context without aesthetic violation (no icons, no gradients, no photography)

---

### GENERATION_PROMPTS

**Single master construction prompt:**

> Create a premium vertical poster (4:5, 1000×1250px) for aight, an Indian AI API platform. Design is typographic-led, black background. Center the price figures ₹9 (image generation) and ₹99 (video generation) in bold geometric sans-serif white type (180–220px). Surround with supporting text in white/gray: "Aight · Prepaid AI for Indian businesses" top; "Set hard caps. Track live. One GST invoice." as subhead; "getaight.ai" footer. Use one saffron or electric indigo accent color for the ₹ symbols and a single thin rule. Include small festive marker: "Build faster this season" as an accent. No photography, icons, or illustrations. Lettering and spacing alone convey premium infrastructure credibility, not retail discount. Poster is suitable for print and digital festive promotion to Indian business audiences.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- Typographic treatment (manual kerning, optical spacing, leading) should be refined post-generation
- Currency symbols (₹) must be precisely placed and color-correct
- Aight brand mark/wordmark placement must align with official brand identity
- Text strings are fixed (no variation):
  - ₹9 / ₹99
  - "Aight · Prepaid AI for Indian businesses"
  - "Set hard caps. Track live. One GST invoice."
  - "getaight.ai"
  - "Build faster this season"

**Design approval gating:**
- Confirm festive tone is subtle, not visually dominant (should not cheapen the brand)
- Verify pricing figures are the dominant visual anchor
- Check that black background and minimal color scheme feel premium, not austere

---

### AUDIO_AND_EDIT

N/A (static image deliverable).

---

### FAILURE_PREVENTION

1. **Price visibility failing:** If ₹9 and ₹99 are not immediately scannable (first 1 second), redesign scale/positioning. Test with rapid eye-track.
2. **Brand confusion:** If the design feels like a retail sale flyer rather than infrastructure product, increase whitespace, reduce festive ornamentation, enforce sober typography.
3. **Readability in digital/small sizes:** Test poster at 500×625px thumbnail; if text collapses, increase font size or adjust hierarchy.
4. **Localization misstep:** Confirm ₹ symbol and Hinglish/English language balance match aight's existing materials (site uses English; this poster should too, with India-first context clear through rupee currency and brand statement).
5. **Color contrast:** Ensure saffron/indigo accent does not create visual noise or reduce premium feel; test against black background for legibility and sophistication.

---

### HARD_CONSTRAINT_CHECK

✅ **4:5 aspect ratio:** Poster dimensions specified and applied  
✅ **Pricing visibility:** ₹9 and ₹99 positioned as primary visual hierarchy  
✅ **Premium tone:** Typography-led, no retail aesthetic, infrastructure credibility maintained  
✅ **Festive season context:** Incorporated as subtle accent ("Build faster this season"), not dominant  
✅ **Indian business target:** Rupee currency, aight's prepaid/GST/founder-support messaging, "hard caps" proof point included  
✅ **Single concept:** One poster design, no alternatives  
✅ **aight brand/product info sourced from official website only:** All messaging grounded in getaight.ai content (prepaid wallet, hard caps, GST, cost control, "Where Indian businesses buy AI")  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (frozen snapshot)
  - Brand positioning: "Where Indian businesses buy AI"
  - Core pillars: prepaid rupee wallet, hard caps, one domestic GST invoice, founder support
  - Product offerings: text (GPT, Claude, Gemini), voice (Sarvam, Smallest, ElevenLabs), image (curated set)
  - Key differentiators: cost control ("Spend you can see"), transparency, India-first infrastructure, minimal onboarding
  - Target customer profile: Indian teams, production AI workflows, cost-conscious enterprises

**No external sources or assumptions were applied beyond the aight website.**

---

## VISUAL_SYSTEM
**Color palette:**
- **Primary:** Deep matte black background (confidence, infrastructure, India-first institutional feel)
- **Type accent:** Crisp white (₹9 and ₹99 figures) and a single secondary color—deep saffron or electric indigo (₹ symbol, thin accent line)—to signal India and modernity without cliché

**Typography:**
- **Headline figures (₹9 / ₹99):** Bold, geometric sans-serif (e.g., Inter Bold, Rigth Grotesk, or similar), sized 180–220px to dominate viewport
- **Body/supporting text:** Lighter weight of same family or neutral sans-serif (e.g., Inter Regular); 18–24px
- **Hierarchy maintained through scale and weight, not color noise**

**Layout structure:**
- Vertical flow: logo/brand mark at top (small, 40–60px)
- Central zone (60–75% of poster): ₹9 and ₹99 positioned left-right or stacked with clear visual separation (thin horizontal line)
- Below pricing: short supporting line ("Image generation · Video generation" or minimal label)
- Mid-poster: one sentence of proof ("Set hard caps. Track live. One GST invoice.")
- Footer (10% of space): small "Aight · getaight.ai"
- Festive note ("Build faster this season") tucked as a thin accent line in one corner or baseline

**Whitespace:** Generous. Allows each element to breathe and signals premium/confidence.

---

### PRODUCTION_RECIPE

1. **Grid structure:** 1000×1250px at 300dpi (poster-quality print)
2. **Base layer:** Black background (#000000 or slight warm-black)
3. **Typesetting passes:**
   - Position and style ₹9 and ₹99 as anchor elements (white, bold, 200px+)
   - Add currency symbol in saffron/indigo accent color (₹)
   - Layer supporting text in hierarchy
   - Apply subtle letter-spacing and line-height to reinforce premium feel
4. **Accent line:** Thin horizontal or vertical rule in saffron/indigo, separating price figures or framing core message
5. **Fine-tuning:** Kerning, baseline alignment, optical spacing for a hand-refined feel (not automatic)
6. **Final pass:** Confirm all text meets festive context without aesthetic violation (no icons, no gradients, no photography)

---

### GENERATION_PROMPTS

**Single master construction prompt:**

> Create a premium vertical poster (4:5, 1000×1250px) for aight, an Indian AI API platform. Design is typographic-led, black background. Center the price figures ₹9 (image generation) and ₹99 (video generation) in bold geometric sans-serif white type (180–220px). Surround with supporting text in white/gray: "Aight · Prepaid AI for Indian businesses" top; "Set hard caps. Track live. One GST invoice." as subhead; "getaight.ai" footer. Use one saffron or electric indigo accent color for the ₹ symbols and a single thin rule. Include small festive marker: "Build faster this season" as an accent. No photography, icons, or illustrations. Lettering and spacing alone convey premium infrastructure credibility, not retail discount. Poster is suitable for print and digital festive promotion to Indian business audiences.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- Typographic treatment (manual kerning, optical spacing, leading) should be refined post-generation
- Currency symbols (₹) must be precisely placed and color-correct
- Aight brand mark/wordmark placement must align with official brand identity
- Text strings are fixed (no variation):
  - ₹9 / ₹99
  - "Aight · Prepaid AI for Indian businesses"
  - "Set hard caps. Track live. One GST invoice."
  - "getaight.ai"
  - "Build faster this season"

**Design approval gating:**
- Confirm festive tone is subtle, not visually dominant (should not cheapen the brand)
- Verify pricing figures are the dominant visual anchor
- Check that black background and minimal color scheme feel premium, not austere

---

### AUDIO_AND_EDIT

N/A (static image deliverable).

---

### FAILURE_PREVENTION

1. **Price visibility failing:** If ₹9 and ₹99 are not immediately scannable (first 1 second), redesign scale/positioning. Test with rapid eye-track.
2. **Brand confusion:** If the design feels like a retail sale flyer rather than infrastructure product, increase whitespace, reduce festive ornamentation, enforce sober typography.
3. **Readability in digital/small sizes:** Test poster at 500×625px thumbnail; if text collapses, increase font size or adjust hierarchy.
4. **Localization misstep:** Confirm ₹ symbol and Hinglish/English language balance match aight's existing materials (site uses English; this poster should too, with India-first context clear through rupee currency and brand statement).
5. **Color contrast:** Ensure saffron/indigo accent does not create visual noise or reduce premium feel; test against black background for legibility and sophistication.

---

### HARD_CONSTRAINT_CHECK

✅ **4:5 aspect ratio:** Poster dimensions specified and applied  
✅ **Pricing visibility:** ₹9 and ₹99 positioned as primary visual hierarchy  
✅ **Premium tone:** Typography-led, no retail aesthetic, infrastructure credibility maintained  
✅ **Festive season context:** Incorporated as subtle accent ("Build faster this season"), not dominant  
✅ **Indian business target:** Rupee currency, aight's prepaid/GST/founder-support messaging, "hard caps" proof point included  
✅ **Single concept:** One poster design, no alternatives  
✅ **aight brand/product info sourced from official website only:** All messaging grounded in getaight.ai content (prepaid wallet, hard caps, GST, cost control, "Where Indian businesses buy AI")  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (frozen snapshot)
  - Brand positioning: "Where Indian businesses buy AI"
  - Core pillars: prepaid rupee wallet, hard caps, one domestic GST invoice, founder support
  - Product offerings: text (GPT, Claude, Gemini), voice (Sarvam, Smallest, ElevenLabs), image (curated set)
  - Key differentiators: cost control ("Spend you can see"), transparency, India-first infrastructure, minimal onboarding
  - Target customer profile: Indian teams, production AI workflows, cost-conscious enterprises

**No external sources or assumptions were applied beyond the aight website.**

---

## PRODUCTION_RECIPE
1. **Grid structure:** 1000×1250px at 300dpi (poster-quality print)
2. **Base layer:** Black background (#000000 or slight warm-black)
3. **Typesetting passes:**
   - Position and style ₹9 and ₹99 as anchor elements (white, bold, 200px+)
   - Add currency symbol in saffron/indigo accent color (₹)
   - Layer supporting text in hierarchy
   - Apply subtle letter-spacing and line-height to reinforce premium feel
4. **Accent line:** Thin horizontal or vertical rule in saffron/indigo, separating price figures or framing core message
5. **Fine-tuning:** Kerning, baseline alignment, optical spacing for a hand-refined feel (not automatic)
6. **Final pass:** Confirm all text meets festive context without aesthetic violation (no icons, no gradients, no photography)

---

### GENERATION_PROMPTS

**Single master construction prompt:**

> Create a premium vertical poster (4:5, 1000×1250px) for aight, an Indian AI API platform. Design is typographic-led, black background. Center the price figures ₹9 (image generation) and ₹99 (video generation) in bold geometric sans-serif white type (180–220px). Surround with supporting text in white/gray: "Aight · Prepaid AI for Indian businesses" top; "Set hard caps. Track live. One GST invoice." as subhead; "getaight.ai" footer. Use one saffron or electric indigo accent color for the ₹ symbols and a single thin rule. Include small festive marker: "Build faster this season" as an accent. No photography, icons, or illustrations. Lettering and spacing alone convey premium infrastructure credibility, not retail discount. Poster is suitable for print and digital festive promotion to Indian business audiences.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- Typographic treatment (manual kerning, optical spacing, leading) should be refined post-generation
- Currency symbols (₹) must be precisely placed and color-correct
- Aight brand mark/wordmark placement must align with official brand identity
- Text strings are fixed (no variation):
  - ₹9 / ₹99
  - "Aight · Prepaid AI for Indian businesses"
  - "Set hard caps. Track live. One GST invoice."
  - "getaight.ai"
  - "Build faster this season"

**Design approval gating:**
- Confirm festive tone is subtle, not visually dominant (should not cheapen the brand)
- Verify pricing figures are the dominant visual anchor
- Check that black background and minimal color scheme feel premium, not austere

---

### AUDIO_AND_EDIT

N/A (static image deliverable).

---

### FAILURE_PREVENTION

1. **Price visibility failing:** If ₹9 and ₹99 are not immediately scannable (first 1 second), redesign scale/positioning. Test with rapid eye-track.
2. **Brand confusion:** If the design feels like a retail sale flyer rather than infrastructure product, increase whitespace, reduce festive ornamentation, enforce sober typography.
3. **Readability in digital/small sizes:** Test poster at 500×625px thumbnail; if text collapses, increase font size or adjust hierarchy.
4. **Localization misstep:** Confirm ₹ symbol and Hinglish/English language balance match aight's existing materials (site uses English; this poster should too, with India-first context clear through rupee currency and brand statement).
5. **Color contrast:** Ensure saffron/indigo accent does not create visual noise or reduce premium feel; test against black background for legibility and sophistication.

---

### HARD_CONSTRAINT_CHECK

✅ **4:5 aspect ratio:** Poster dimensions specified and applied  
✅ **Pricing visibility:** ₹9 and ₹99 positioned as primary visual hierarchy  
✅ **Premium tone:** Typography-led, no retail aesthetic, infrastructure credibility maintained  
✅ **Festive season context:** Incorporated as subtle accent ("Build faster this season"), not dominant  
✅ **Indian business target:** Rupee currency, aight's prepaid/GST/founder-support messaging, "hard caps" proof point included  
✅ **Single concept:** One poster design, no alternatives  
✅ **aight brand/product info sourced from official website only:** All messaging grounded in getaight.ai content (prepaid wallet, hard caps, GST, cost control, "Where Indian businesses buy AI")  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (frozen snapshot)
  - Brand positioning: "Where Indian businesses buy AI"
  - Core pillars: prepaid rupee wallet, hard caps, one domestic GST invoice, founder support
  - Product offerings: text (GPT, Claude, Gemini), voice (Sarvam, Smallest, ElevenLabs), image (curated set)
  - Key differentiators: cost control ("Spend you can see"), transparency, India-first infrastructure, minimal onboarding
  - Target customer profile: Indian teams, production AI workflows, cost-conscious enterprises

**No external sources or assumptions were applied beyond the aight website.**

---

## GENERATION_PROMPTS
**Single master construction prompt:**

> Create a premium vertical poster (4:5, 1000×1250px) for aight, an Indian AI API platform. Design is typographic-led, black background. Center the price figures ₹9 (image generation) and ₹99 (video generation) in bold geometric sans-serif white type (180–220px). Surround with supporting text in white/gray: "Aight · Prepaid AI for Indian businesses" top; "Set hard caps. Track live. One GST invoice." as subhead; "getaight.ai" footer. Use one saffron or electric indigo accent color for the ₹ symbols and a single thin rule. Include small festive marker: "Build faster this season" as an accent. No photography, icons, or illustrations. Lettering and spacing alone convey premium infrastructure credibility, not retail discount. Poster is suitable for print and digital festive promotion to Indian business audiences.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- Typographic treatment (manual kerning, optical spacing, leading) should be refined post-generation
- Currency symbols (₹) must be precisely placed and color-correct
- Aight brand mark/wordmark placement must align with official brand identity
- Text strings are fixed (no variation):
  - ₹9 / ₹99
  - "Aight · Prepaid AI for Indian businesses"
  - "Set hard caps. Track live. One GST invoice."
  - "getaight.ai"
  - "Build faster this season"

**Design approval gating:**
- Confirm festive tone is subtle, not visually dominant (should not cheapen the brand)
- Verify pricing figures are the dominant visual anchor
- Check that black background and minimal color scheme feel premium, not austere

---

### AUDIO_AND_EDIT

N/A (static image deliverable).

---

### FAILURE_PREVENTION

1. **Price visibility failing:** If ₹9 and ₹99 are not immediately scannable (first 1 second), redesign scale/positioning. Test with rapid eye-track.
2. **Brand confusion:** If the design feels like a retail sale flyer rather than infrastructure product, increase whitespace, reduce festive ornamentation, enforce sober typography.
3. **Readability in digital/small sizes:** Test poster at 500×625px thumbnail; if text collapses, increase font size or adjust hierarchy.
4. **Localization misstep:** Confirm ₹ symbol and Hinglish/English language balance match aight's existing materials (site uses English; this poster should too, with India-first context clear through rupee currency and brand statement).
5. **Color contrast:** Ensure saffron/indigo accent does not create visual noise or reduce premium feel; test against black background for legibility and sophistication.

---

### HARD_CONSTRAINT_CHECK

✅ **4:5 aspect ratio:** Poster dimensions specified and applied  
✅ **Pricing visibility:** ₹9 and ₹99 positioned as primary visual hierarchy  
✅ **Premium tone:** Typography-led, no retail aesthetic, infrastructure credibility maintained  
✅ **Festive season context:** Incorporated as subtle accent ("Build faster this season"), not dominant  
✅ **Indian business target:** Rupee currency, aight's prepaid/GST/founder-support messaging, "hard caps" proof point included  
✅ **Single concept:** One poster design, no alternatives  
✅ **aight brand/product info sourced from official website only:** All messaging grounded in getaight.ai content (prepaid wallet, hard caps, GST, cost control, "Where Indian businesses buy AI")  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (frozen snapshot)
  - Brand positioning: "Where Indian businesses buy AI"
  - Core pillars: prepaid rupee wallet, hard caps, one domestic GST invoice, founder support
  - Product offerings: text (GPT, Claude, Gemini), voice (Sarvam, Smallest, ElevenLabs), image (curated set)
  - Key differentiators: cost control ("Spend you can see"), transparency, India-first infrastructure, minimal onboarding
  - Target customer profile: Indian teams, production AI workflows, cost-conscious enterprises

**No external sources or assumptions were applied beyond the aight website.**

---

## DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS
- Typographic treatment (manual kerning, optical spacing, leading) should be refined post-generation
- Currency symbols (₹) must be precisely placed and color-correct
- Aight brand mark/wordmark placement must align with official brand identity
- Text strings are fixed (no variation):
  - ₹9 / ₹99
  - "Aight · Prepaid AI for Indian businesses"
  - "Set hard caps. Track live. One GST invoice."
  - "getaight.ai"
  - "Build faster this season"

**Design approval gating:**
- Confirm festive tone is subtle, not visually dominant (should not cheapen the brand)
- Verify pricing figures are the dominant visual anchor
- Check that black background and minimal color scheme feel premium, not austere

---

### AUDIO_AND_EDIT

N/A (static image deliverable).

---

### FAILURE_PREVENTION

1. **Price visibility failing:** If ₹9 and ₹99 are not immediately scannable (first 1 second), redesign scale/positioning. Test with rapid eye-track.
2. **Brand confusion:** If the design feels like a retail sale flyer rather than infrastructure product, increase whitespace, reduce festive ornamentation, enforce sober typography.
3. **Readability in digital/small sizes:** Test poster at 500×625px thumbnail; if text collapses, increase font size or adjust hierarchy.
4. **Localization misstep:** Confirm ₹ symbol and Hinglish/English language balance match aight's existing materials (site uses English; this poster should too, with India-first context clear through rupee currency and brand statement).
5. **Color contrast:** Ensure saffron/indigo accent does not create visual noise or reduce premium feel; test against black background for legibility and sophistication.

---

### HARD_CONSTRAINT_CHECK

✅ **4:5 aspect ratio:** Poster dimensions specified and applied  
✅ **Pricing visibility:** ₹9 and ₹99 positioned as primary visual hierarchy  
✅ **Premium tone:** Typography-led, no retail aesthetic, infrastructure credibility maintained  
✅ **Festive season context:** Incorporated as subtle accent ("Build faster this season"), not dominant  
✅ **Indian business target:** Rupee currency, aight's prepaid/GST/founder-support messaging, "hard caps" proof point included  
✅ **Single concept:** One poster design, no alternatives  
✅ **aight brand/product info sourced from official website only:** All messaging grounded in getaight.ai content (prepaid wallet, hard caps, GST, cost control, "Where Indian businesses buy AI")  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (frozen snapshot)
  - Brand positioning: "Where Indian businesses buy AI"
  - Core pillars: prepaid rupee wallet, hard caps, one domestic GST invoice, founder support
  - Product offerings: text (GPT, Claude, Gemini), voice (Sarvam, Smallest, ElevenLabs), image (curated set)
  - Key differentiators: cost control ("Spend you can see"), transparency, India-first infrastructure, minimal onboarding
  - Target customer profile: Indian teams, production AI workflows, cost-conscious enterprises

**No external sources or assumptions were applied beyond the aight website.**

---

## FAILURE_PREVENTION
1. **Price visibility failing:** If ₹9 and ₹99 are not immediately scannable (first 1 second), redesign scale/positioning. Test with rapid eye-track.
2. **Brand confusion:** If the design feels like a retail sale flyer rather than infrastructure product, increase whitespace, reduce festive ornamentation, enforce sober typography.
3. **Readability in digital/small sizes:** Test poster at 500×625px thumbnail; if text collapses, increase font size or adjust hierarchy.
4. **Localization misstep:** Confirm ₹ symbol and Hinglish/English language balance match aight's existing materials (site uses English; this poster should too, with India-first context clear through rupee currency and brand statement).
5. **Color contrast:** Ensure saffron/indigo accent does not create visual noise or reduce premium feel; test against black background for legibility and sophistication.

---

### HARD_CONSTRAINT_CHECK

✅ **4:5 aspect ratio:** Poster dimensions specified and applied  
✅ **Pricing visibility:** ₹9 and ₹99 positioned as primary visual hierarchy  
✅ **Premium tone:** Typography-led, no retail aesthetic, infrastructure credibility maintained  
✅ **Festive season context:** Incorporated as subtle accent ("Build faster this season"), not dominant  
✅ **Indian business target:** Rupee currency, aight's prepaid/GST/founder-support messaging, "hard caps" proof point included  
✅ **Single concept:** One poster design, no alternatives  
✅ **aight brand/product info sourced from official website only:** All messaging grounded in getaight.ai content (prepaid wallet, hard caps, GST, cost control, "Where Indian businesses buy AI")  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (frozen snapshot)
  - Brand positioning: "Where Indian businesses buy AI"
  - Core pillars: prepaid rupee wallet, hard caps, one domestic GST invoice, founder support
  - Product offerings: text (GPT, Claude, Gemini), voice (Sarvam, Smallest, ElevenLabs), image (curated set)
  - Key differentiators: cost control ("Spend you can see"), transparency, India-first infrastructure, minimal onboarding
  - Target customer profile: Indian teams, production AI workflows, cost-conscious enterprises

**No external sources or assumptions were applied beyond the aight website.**

---

## HARD_CONSTRAINT_CHECK
✅ **4:5 aspect ratio:** Poster dimensions specified and applied  
✅ **Pricing visibility:** ₹9 and ₹99 positioned as primary visual hierarchy  
✅ **Premium tone:** Typography-led, no retail aesthetic, infrastructure credibility maintained  
✅ **Festive season context:** Incorporated as subtle accent ("Build faster this season"), not dominant  
✅ **Indian business target:** Rupee currency, aight's prepaid/GST/founder-support messaging, "hard caps" proof point included  
✅ **Single concept:** One poster design, no alternatives  
✅ **aight brand/product info sourced from official website only:** All messaging grounded in getaight.ai content (prepaid wallet, hard caps, GST, cost control, "Where Indian businesses buy AI")  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (frozen snapshot)
  - Brand positioning: "Where Indian businesses buy AI"
  - Core pillars: prepaid rupee wallet, hard caps, one domestic GST invoice, founder support
  - Product offerings: text (GPT, Claude, Gemini), voice (Sarvam, Smallest, ElevenLabs), image (curated set)
  - Key differentiators: cost control ("Spend you can see"), transparency, India-first infrastructure, minimal onboarding
  - Target customer profile: Indian teams, production AI workflows, cost-conscious enterprises

**No external sources or assumptions were applied beyond the aight website.**

---

## GENERATE I01
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I02 — B02

Source key: E037-haiku-no-canon-B02-R2
Use frozen brief B02 from the top of this file.



## GENERATE I02
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I03 — B02

Source key: E037-haiku-no-canon-B02-R3
Use frozen brief B02 from the top of this file.

## DELIVERABLE
One premium 4:5 vertical promotional poster (2160 × 2700 px) for Indian festive season.

---

### OBJECTIVE_INTERPRETATION
Market Aight's media generation products (image at ₹9, video at ₹99) to Indian businesses during festive season. Position pricing as professionally accessible value—not a discount—reflecting Aight's actual brand positioning: "Where Indian businesses buy AI." Pricing must be the communication anchor, but visual/typographic treatment must convey infrastructure-grade legitimacy and premium quality.

---

### CORE_CREATIVE_IDEA
**"Premium pricing transparency as brand authority."**

The poster places pricing front-and-center not as a promotional hook but as a statement of clarity and honesty—mirroring Aight's brand claim: "Spend you can see. Rupees that behave." Typography hierarchy, whitespace discipline, and restrained festive visual language position this as a serious technology company that happens to price fairly. The design says: *"We're confident enough in our infrastructure to let pricing speak."*

---

### MESSAGE_AND_INFORMATION_HIERARCHY

1. **Hero level** (50% visual/typographic weight): Pricing statement  
   - `IMAGE: ₹9` and `VIDEO: ₹99` as dominant typographic anchors
   - Positioned in visual center; instantly readable at thumb distance

2. **Secondary level** (30% weight): Product clarification + value framing  
   - `Image Generation` and `Video Generation` as product descriptors
   - Brief value statement: "AI that works for Indian business"
   
3. **Tertiary level** (15% weight): Festive context + call-to-action  
   - Light festive visual signal (not overwhelming)
   - Subtle urgency tie-in: "This festive season"
   - Soft CTA: "getaight.ai" or "Talk to us"

4. **Footer** (5% weight): Brand confirmation  
   - Aight logo and tagline: "Where Indian businesses buy AI"

---

### VISUAL_SYSTEM

**Color Palette:**
- **Primary background**: Deep charcoal or near-black (professional, infrastructure-grade)
- **Pricing highlight**: Warm gold or muted saffron accent (festive restraint, no neon)
- **Text**: Off-white/cream for maximum legibility
- **Accent**: Single secondary color (perhaps a muted deep green or rust) for product descriptor blocks

**Typography:**
- **Pricing numbers** (`₹9`, `₹99`): XL geometric sans-serif, bold weight; approx. 180–240pt
- **Product labels** (`Image`, `Video`, `Generation`): Clean sans-serif, 48–64pt, medium weight
- **Body/supporting text**: 28–36pt, light-to-regular weight, generous line spacing for air
- **Tagline/footer**: 20–24pt, light weight

**Spatial Layout:**
- Centered vertical axis; symmetrical balance
- Large whitespace above and below pricing; breathing room is part of the premium signal
- Product labels flanking pricing with subtle dividing lines or geometric shapes (icons optional)
- Minimal decorative elements; geometric shapes only if they enhance clarity

**Festive Visual Signal:**
- One optional subtle geometric/pattern element (e.g., simplified mandala edge motif, thin line work, corner details) in 10–15% opacity, positioned at edges
- No illustration, no clutter
- Diwali/Navratri/Dussehra association conveyed through color warmth + restraint, not visual noise

---

### PRODUCTION_RECIPE

1. **Base composition**: Center-aligned vertical poster, dark background, three visual zones
2. **Zone 1 (Top 20%)**: Aight branding and tagline, small and clear
3. **Zone 2 (Middle 60%)**: Pricing and product hierarchy
   - Left column: `IMAGE` + `₹9`
   - Center spacing
   - Right column: `VIDEO` + `₹99`
   - Unified under umbrella phrase: "AI that works for Indian business"
4. **Zone 3 (Bottom 20%)**: Festive context, subtle urgency, CTA, footer
5. **Apply**: Premium sans-serif throughout; no more than 2–3 font weights; white space discipline

---

### GENERATION_PROMPTS

**Single integrated final prompt:**

```
Create a premium 4:5 vertical promotional poster for Aight, an Indian AI API platform. 
Dark charcoal background. Center-aligned layout with generous whitespace. 

Top section (small): "Aight" wordmark / logo and tagline "Where Indian businesses buy AI" in light sans-serif, ~20pt, off-white.

Middle section (dominant): 
Left side: "IMAGE" in bold sans-serif ~48pt, underneath "₹9" in extra-bold geometric sans-serif ~200pt, warm gold/muted saffron color.
Right side: "VIDEO" in bold sans-serif ~48pt, underneath "₹99" in extra-bold geometric sans-serif ~200pt, same warm gold/saffron.
Subtle vertical dividing line or thin geometric accent between them.
Beneath both: "Generation" in smaller serif or refined sans ~36pt, off-white; OR unified label "AI Media Generation."

Below pricing: Small supporting line in light gray, ~28pt: "AI that works for Indian business" OR "Designed for India."

Bottom section: 
Light festive visual hint—optional thin geometric mandala or corner line pattern in 10–15% opacity, warm gold. 
Soft CTA: "This festive season" (optional, small) + "getaight.ai" in 24pt, light weight, off-white.
Footer line: "One domestic invoice. Spend you can see." or similar brand voice, ~18pt, very light gray.

Mood: Serious technology company, premium infrastructure grade, confident pricing transparency. No discount-flyer energy. Professional, clean, minimal. High-end luxury restrain rather than festive chaos.
```

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Use templated design system (not AI generation):**
- Vector-based poster built in professional design tool (Figma, Adobe InDesign, Illustrator)
- Rationale: Pricing, logo, and precise typographic hierarchy require pixel-perfect control; AI image generation introduces unwanted style drift and OCR risk on critical text

**Elements to build deterministically:**
- Aight logo (source from brand files if available; if not, use text-based wordmark)
- All typography (font selection, sizing, kerning, leading)
- Geometric dividers, spacing, background color
- Festive pattern/motif (custom vector or minimal stock graphic, positioned and opacity-controlled precisely)

---

### AUDIO_AND_EDIT

**Not applicable.** This is a static poster. No audio or video editing.

---

### FAILURE_PREVENTION

| Failure Mode | Prevention |
|---|---|
| Pricing gets lost in visual noise | Typography does 90% of work; pricing is largest element; dark background isolates prices |
| Looks like discount flyer, not infrastructure brand | Whitespace discipline, no exclamation marks, one color accent only, professional sans-serif, restraint on festive signals |
| Pricing not immediately readable at mobile distance | ₹9 and ₹99 occupy ~25% of poster height; geometric sans-serif chosen for clarity; no serif confusion on numbers |
| Festive signal overwhelms professionalism | Festive visual = <15% opacity, edge-positioned, geometric only, no illustration |
| GST/billing confusion | Include small line like "One domestic invoice" or "Spend you can see"—reinforces Aight brand voice |
| Call-to-action unclear | Use "getaight.ai" prominently at bottom; optional WhatsApp or "Talk to us" secondary |
| Font kerning/spacing errors on prices | Use production design tool (Figga/InDesign), not AI; manually kern if needed |
| Layout breaks on print or rescale | Build at 2160×2700, test at 1080×1350 and larger; use relative spacing units |

---

### HARD_CONSTRAINT_CHECK

✅ **One poster only** → Delivered as single 4:5 asset  
✅ **Pricing immediately understandable** → ₹9 and ₹99 dominate visual center, largest elements  
✅ **Serious AI infrastructure company feel** → Professional typography, whitespace, minimal decoration, no retail language  
✅ **Typography and hierarchy do most work** → Minimal imagery, design is type-forward  
✅ **Festive season relevance** → Subtle warm-tone accent, optional light geometric motif, "This festive season" optional callout  
✅ **4:5 format** → Vertical poster optimized for mobile/social/print distribution  
✅ **Used only getaight.ai for product/brand info** → All brand voice, product info, tagline sourced from website  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Website used:** https://getaight.ai (frozen snapshot)

**Information extracted and applied:**
- Brand tagline: *"Where Indian businesses buy AI"*
- Core brand values: Transparency, domestic GST invoice, prepaid rupees, "Spend you can see"
- Product mention: Image and voice models ("Image: A curated set")
- Brand voice: Professional, founder-led, honest about control and ROI
- Target audience: Indian businesses (production AI teams, founders, product leaders)
- Positioning: Not a discount play; infrastructure quality with fair pricing and hands-on support

**Specific phrases/tonality borrowed:**
- "Spend you can see. Rupees that behave." → Informs "One domestic invoice" supporting line
- No mention of video pricing on live site, but customer specified ₹99 video; accepted as valid commercial proposition for this festive promotion

---

**END PRODUCTION PACKAGE**

## OBJECTIVE_INTERPRETATION
Market Aight's media generation products (image at ₹9, video at ₹99) to Indian businesses during festive season. Position pricing as professionally accessible value—not a discount—reflecting Aight's actual brand positioning: "Where Indian businesses buy AI." Pricing must be the communication anchor, but visual/typographic treatment must convey infrastructure-grade legitimacy and premium quality.

---

### CORE_CREATIVE_IDEA
**"Premium pricing transparency as brand authority."**

The poster places pricing front-and-center not as a promotional hook but as a statement of clarity and honesty—mirroring Aight's brand claim: "Spend you can see. Rupees that behave." Typography hierarchy, whitespace discipline, and restrained festive visual language position this as a serious technology company that happens to price fairly. The design says: *"We're confident enough in our infrastructure to let pricing speak."*

---

### MESSAGE_AND_INFORMATION_HIERARCHY

1. **Hero level** (50% visual/typographic weight): Pricing statement  
   - `IMAGE: ₹9` and `VIDEO: ₹99` as dominant typographic anchors
   - Positioned in visual center; instantly readable at thumb distance

2. **Secondary level** (30% weight): Product clarification + value framing  
   - `Image Generation` and `Video Generation` as product descriptors
   - Brief value statement: "AI that works for Indian business"
   
3. **Tertiary level** (15% weight): Festive context + call-to-action  
   - Light festive visual signal (not overwhelming)
   - Subtle urgency tie-in: "This festive season"
   - Soft CTA: "getaight.ai" or "Talk to us"

4. **Footer** (5% weight): Brand confirmation  
   - Aight logo and tagline: "Where Indian businesses buy AI"

---

### VISUAL_SYSTEM

**Color Palette:**
- **Primary background**: Deep charcoal or near-black (professional, infrastructure-grade)
- **Pricing highlight**: Warm gold or muted saffron accent (festive restraint, no neon)
- **Text**: Off-white/cream for maximum legibility
- **Accent**: Single secondary color (perhaps a muted deep green or rust) for product descriptor blocks

**Typography:**
- **Pricing numbers** (`₹9`, `₹99`): XL geometric sans-serif, bold weight; approx. 180–240pt
- **Product labels** (`Image`, `Video`, `Generation`): Clean sans-serif, 48–64pt, medium weight
- **Body/supporting text**: 28–36pt, light-to-regular weight, generous line spacing for air
- **Tagline/footer**: 20–24pt, light weight

**Spatial Layout:**
- Centered vertical axis; symmetrical balance
- Large whitespace above and below pricing; breathing room is part of the premium signal
- Product labels flanking pricing with subtle dividing lines or geometric shapes (icons optional)
- Minimal decorative elements; geometric shapes only if they enhance clarity

**Festive Visual Signal:**
- One optional subtle geometric/pattern element (e.g., simplified mandala edge motif, thin line work, corner details) in 10–15% opacity, positioned at edges
- No illustration, no clutter
- Diwali/Navratri/Dussehra association conveyed through color warmth + restraint, not visual noise

---

### PRODUCTION_RECIPE

1. **Base composition**: Center-aligned vertical poster, dark background, three visual zones
2. **Zone 1 (Top 20%)**: Aight branding and tagline, small and clear
3. **Zone 2 (Middle 60%)**: Pricing and product hierarchy
   - Left column: `IMAGE` + `₹9`
   - Center spacing
   - Right column: `VIDEO` + `₹99`
   - Unified under umbrella phrase: "AI that works for Indian business"
4. **Zone 3 (Bottom 20%)**: Festive context, subtle urgency, CTA, footer
5. **Apply**: Premium sans-serif throughout; no more than 2–3 font weights; white space discipline

---

### GENERATION_PROMPTS

**Single integrated final prompt:**

```
Create a premium 4:5 vertical promotional poster for Aight, an Indian AI API platform. 
Dark charcoal background. Center-aligned layout with generous whitespace. 

Top section (small): "Aight" wordmark / logo and tagline "Where Indian businesses buy AI" in light sans-serif, ~20pt, off-white.

Middle section (dominant): 
Left side: "IMAGE" in bold sans-serif ~48pt, underneath "₹9" in extra-bold geometric sans-serif ~200pt, warm gold/muted saffron color.
Right side: "VIDEO" in bold sans-serif ~48pt, underneath "₹99" in extra-bold geometric sans-serif ~200pt, same warm gold/saffron.
Subtle vertical dividing line or thin geometric accent between them.
Beneath both: "Generation" in smaller serif or refined sans ~36pt, off-white; OR unified label "AI Media Generation."

Below pricing: Small supporting line in light gray, ~28pt: "AI that works for Indian business" OR "Designed for India."

Bottom section: 
Light festive visual hint—optional thin geometric mandala or corner line pattern in 10–15% opacity, warm gold. 
Soft CTA: "This festive season" (optional, small) + "getaight.ai" in 24pt, light weight, off-white.
Footer line: "One domestic invoice. Spend you can see." or similar brand voice, ~18pt, very light gray.

Mood: Serious technology company, premium infrastructure grade, confident pricing transparency. No discount-flyer energy. Professional, clean, minimal. High-end luxury restrain rather than festive chaos.
```

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Use templated design system (not AI generation):**
- Vector-based poster built in professional design tool (Figma, Adobe InDesign, Illustrator)
- Rationale: Pricing, logo, and precise typographic hierarchy require pixel-perfect control; AI image generation introduces unwanted style drift and OCR risk on critical text

**Elements to build deterministically:**
- Aight logo (source from brand files if available; if not, use text-based wordmark)
- All typography (font selection, sizing, kerning, leading)
- Geometric dividers, spacing, background color
- Festive pattern/motif (custom vector or minimal stock graphic, positioned and opacity-controlled precisely)

---

### AUDIO_AND_EDIT

**Not applicable.** This is a static poster. No audio or video editing.

---

### FAILURE_PREVENTION

| Failure Mode | Prevention |
|---|---|
| Pricing gets lost in visual noise | Typography does 90% of work; pricing is largest element; dark background isolates prices |
| Looks like discount flyer, not infrastructure brand | Whitespace discipline, no exclamation marks, one color accent only, professional sans-serif, restraint on festive signals |
| Pricing not immediately readable at mobile distance | ₹9 and ₹99 occupy ~25% of poster height; geometric sans-serif chosen for clarity; no serif confusion on numbers |
| Festive signal overwhelms professionalism | Festive visual = <15% opacity, edge-positioned, geometric only, no illustration |
| GST/billing confusion | Include small line like "One domestic invoice" or "Spend you can see"—reinforces Aight brand voice |
| Call-to-action unclear | Use "getaight.ai" prominently at bottom; optional WhatsApp or "Talk to us" secondary |
| Font kerning/spacing errors on prices | Use production design tool (Figga/InDesign), not AI; manually kern if needed |
| Layout breaks on print or rescale | Build at 2160×2700, test at 1080×1350 and larger; use relative spacing units |

---

### HARD_CONSTRAINT_CHECK

✅ **One poster only** → Delivered as single 4:5 asset  
✅ **Pricing immediately understandable** → ₹9 and ₹99 dominate visual center, largest elements  
✅ **Serious AI infrastructure company feel** → Professional typography, whitespace, minimal decoration, no retail language  
✅ **Typography and hierarchy do most work** → Minimal imagery, design is type-forward  
✅ **Festive season relevance** → Subtle warm-tone accent, optional light geometric motif, "This festive season" optional callout  
✅ **4:5 format** → Vertical poster optimized for mobile/social/print distribution  
✅ **Used only getaight.ai for product/brand info** → All brand voice, product info, tagline sourced from website  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Website used:** https://getaight.ai (frozen snapshot)

**Information extracted and applied:**
- Brand tagline: *"Where Indian businesses buy AI"*
- Core brand values: Transparency, domestic GST invoice, prepaid rupees, "Spend you can see"
- Product mention: Image and voice models ("Image: A curated set")
- Brand voice: Professional, founder-led, honest about control and ROI
- Target audience: Indian businesses (production AI teams, founders, product leaders)
- Positioning: Not a discount play; infrastructure quality with fair pricing and hands-on support

**Specific phrases/tonality borrowed:**
- "Spend you can see. Rupees that behave." → Informs "One domestic invoice" supporting line
- No mention of video pricing on live site, but customer specified ₹99 video; accepted as valid commercial proposition for this festive promotion

---

**END PRODUCTION PACKAGE**

## CORE_CREATIVE_IDEA
**"Premium pricing transparency as brand authority."**

The poster places pricing front-and-center not as a promotional hook but as a statement of clarity and honesty—mirroring Aight's brand claim: "Spend you can see. Rupees that behave." Typography hierarchy, whitespace discipline, and restrained festive visual language position this as a serious technology company that happens to price fairly. The design says: *"We're confident enough in our infrastructure to let pricing speak."*

---

### MESSAGE_AND_INFORMATION_HIERARCHY

1. **Hero level** (50% visual/typographic weight): Pricing statement  
   - `IMAGE: ₹9` and `VIDEO: ₹99` as dominant typographic anchors
   - Positioned in visual center; instantly readable at thumb distance

2. **Secondary level** (30% weight): Product clarification + value framing  
   - `Image Generation` and `Video Generation` as product descriptors
   - Brief value statement: "AI that works for Indian business"
   
3. **Tertiary level** (15% weight): Festive context + call-to-action  
   - Light festive visual signal (not overwhelming)
   - Subtle urgency tie-in: "This festive season"
   - Soft CTA: "getaight.ai" or "Talk to us"

4. **Footer** (5% weight): Brand confirmation  
   - Aight logo and tagline: "Where Indian businesses buy AI"

---

### VISUAL_SYSTEM

**Color Palette:**
- **Primary background**: Deep charcoal or near-black (professional, infrastructure-grade)
- **Pricing highlight**: Warm gold or muted saffron accent (festive restraint, no neon)
- **Text**: Off-white/cream for maximum legibility
- **Accent**: Single secondary color (perhaps a muted deep green or rust) for product descriptor blocks

**Typography:**
- **Pricing numbers** (`₹9`, `₹99`): XL geometric sans-serif, bold weight; approx. 180–240pt
- **Product labels** (`Image`, `Video`, `Generation`): Clean sans-serif, 48–64pt, medium weight
- **Body/supporting text**: 28–36pt, light-to-regular weight, generous line spacing for air
- **Tagline/footer**: 20–24pt, light weight

**Spatial Layout:**
- Centered vertical axis; symmetrical balance
- Large whitespace above and below pricing; breathing room is part of the premium signal
- Product labels flanking pricing with subtle dividing lines or geometric shapes (icons optional)
- Minimal decorative elements; geometric shapes only if they enhance clarity

**Festive Visual Signal:**
- One optional subtle geometric/pattern element (e.g., simplified mandala edge motif, thin line work, corner details) in 10–15% opacity, positioned at edges
- No illustration, no clutter
- Diwali/Navratri/Dussehra association conveyed through color warmth + restraint, not visual noise

---

### PRODUCTION_RECIPE

1. **Base composition**: Center-aligned vertical poster, dark background, three visual zones
2. **Zone 1 (Top 20%)**: Aight branding and tagline, small and clear
3. **Zone 2 (Middle 60%)**: Pricing and product hierarchy
   - Left column: `IMAGE` + `₹9`
   - Center spacing
   - Right column: `VIDEO` + `₹99`
   - Unified under umbrella phrase: "AI that works for Indian business"
4. **Zone 3 (Bottom 20%)**: Festive context, subtle urgency, CTA, footer
5. **Apply**: Premium sans-serif throughout; no more than 2–3 font weights; white space discipline

---

### GENERATION_PROMPTS

**Single integrated final prompt:**

```
Create a premium 4:5 vertical promotional poster for Aight, an Indian AI API platform. 
Dark charcoal background. Center-aligned layout with generous whitespace. 

Top section (small): "Aight" wordmark / logo and tagline "Where Indian businesses buy AI" in light sans-serif, ~20pt, off-white.

Middle section (dominant): 
Left side: "IMAGE" in bold sans-serif ~48pt, underneath "₹9" in extra-bold geometric sans-serif ~200pt, warm gold/muted saffron color.
Right side: "VIDEO" in bold sans-serif ~48pt, underneath "₹99" in extra-bold geometric sans-serif ~200pt, same warm gold/saffron.
Subtle vertical dividing line or thin geometric accent between them.
Beneath both: "Generation" in smaller serif or refined sans ~36pt, off-white; OR unified label "AI Media Generation."

Below pricing: Small supporting line in light gray, ~28pt: "AI that works for Indian business" OR "Designed for India."

Bottom section: 
Light festive visual hint—optional thin geometric mandala or corner line pattern in 10–15% opacity, warm gold. 
Soft CTA: "This festive season" (optional, small) + "getaight.ai" in 24pt, light weight, off-white.
Footer line: "One domestic invoice. Spend you can see." or similar brand voice, ~18pt, very light gray.

Mood: Serious technology company, premium infrastructure grade, confident pricing transparency. No discount-flyer energy. Professional, clean, minimal. High-end luxury restrain rather than festive chaos.
```

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Use templated design system (not AI generation):**
- Vector-based poster built in professional design tool (Figma, Adobe InDesign, Illustrator)
- Rationale: Pricing, logo, and precise typographic hierarchy require pixel-perfect control; AI image generation introduces unwanted style drift and OCR risk on critical text

**Elements to build deterministically:**
- Aight logo (source from brand files if available; if not, use text-based wordmark)
- All typography (font selection, sizing, kerning, leading)
- Geometric dividers, spacing, background color
- Festive pattern/motif (custom vector or minimal stock graphic, positioned and opacity-controlled precisely)

---

### AUDIO_AND_EDIT

**Not applicable.** This is a static poster. No audio or video editing.

---

### FAILURE_PREVENTION

| Failure Mode | Prevention |
|---|---|
| Pricing gets lost in visual noise | Typography does 90% of work; pricing is largest element; dark background isolates prices |
| Looks like discount flyer, not infrastructure brand | Whitespace discipline, no exclamation marks, one color accent only, professional sans-serif, restraint on festive signals |
| Pricing not immediately readable at mobile distance | ₹9 and ₹99 occupy ~25% of poster height; geometric sans-serif chosen for clarity; no serif confusion on numbers |
| Festive signal overwhelms professionalism | Festive visual = <15% opacity, edge-positioned, geometric only, no illustration |
| GST/billing confusion | Include small line like "One domestic invoice" or "Spend you can see"—reinforces Aight brand voice |
| Call-to-action unclear | Use "getaight.ai" prominently at bottom; optional WhatsApp or "Talk to us" secondary |
| Font kerning/spacing errors on prices | Use production design tool (Figga/InDesign), not AI; manually kern if needed |
| Layout breaks on print or rescale | Build at 2160×2700, test at 1080×1350 and larger; use relative spacing units |

---

### HARD_CONSTRAINT_CHECK

✅ **One poster only** → Delivered as single 4:5 asset  
✅ **Pricing immediately understandable** → ₹9 and ₹99 dominate visual center, largest elements  
✅ **Serious AI infrastructure company feel** → Professional typography, whitespace, minimal decoration, no retail language  
✅ **Typography and hierarchy do most work** → Minimal imagery, design is type-forward  
✅ **Festive season relevance** → Subtle warm-tone accent, optional light geometric motif, "This festive season" optional callout  
✅ **4:5 format** → Vertical poster optimized for mobile/social/print distribution  
✅ **Used only getaight.ai for product/brand info** → All brand voice, product info, tagline sourced from website  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Website used:** https://getaight.ai (frozen snapshot)

**Information extracted and applied:**
- Brand tagline: *"Where Indian businesses buy AI"*
- Core brand values: Transparency, domestic GST invoice, prepaid rupees, "Spend you can see"
- Product mention: Image and voice models ("Image: A curated set")
- Brand voice: Professional, founder-led, honest about control and ROI
- Target audience: Indian businesses (production AI teams, founders, product leaders)
- Positioning: Not a discount play; infrastructure quality with fair pricing and hands-on support

**Specific phrases/tonality borrowed:**
- "Spend you can see. Rupees that behave." → Informs "One domestic invoice" supporting line
- No mention of video pricing on live site, but customer specified ₹99 video; accepted as valid commercial proposition for this festive promotion

---

**END PRODUCTION PACKAGE**

## MESSAGE_AND_INFORMATION_HIERARCHY
1. **Hero level** (50% visual/typographic weight): Pricing statement  
   - `IMAGE: ₹9` and `VIDEO: ₹99` as dominant typographic anchors
   - Positioned in visual center; instantly readable at thumb distance

2. **Secondary level** (30% weight): Product clarification + value framing  
   - `Image Generation` and `Video Generation` as product descriptors
   - Brief value statement: "AI that works for Indian business"
   
3. **Tertiary level** (15% weight): Festive context + call-to-action  
   - Light festive visual signal (not overwhelming)
   - Subtle urgency tie-in: "This festive season"
   - Soft CTA: "getaight.ai" or "Talk to us"

4. **Footer** (5% weight): Brand confirmation  
   - Aight logo and tagline: "Where Indian businesses buy AI"

---

### VISUAL_SYSTEM

**Color Palette:**
- **Primary background**: Deep charcoal or near-black (professional, infrastructure-grade)
- **Pricing highlight**: Warm gold or muted saffron accent (festive restraint, no neon)
- **Text**: Off-white/cream for maximum legibility
- **Accent**: Single secondary color (perhaps a muted deep green or rust) for product descriptor blocks

**Typography:**
- **Pricing numbers** (`₹9`, `₹99`): XL geometric sans-serif, bold weight; approx. 180–240pt
- **Product labels** (`Image`, `Video`, `Generation`): Clean sans-serif, 48–64pt, medium weight
- **Body/supporting text**: 28–36pt, light-to-regular weight, generous line spacing for air
- **Tagline/footer**: 20–24pt, light weight

**Spatial Layout:**
- Centered vertical axis; symmetrical balance
- Large whitespace above and below pricing; breathing room is part of the premium signal
- Product labels flanking pricing with subtle dividing lines or geometric shapes (icons optional)
- Minimal decorative elements; geometric shapes only if they enhance clarity

**Festive Visual Signal:**
- One optional subtle geometric/pattern element (e.g., simplified mandala edge motif, thin line work, corner details) in 10–15% opacity, positioned at edges
- No illustration, no clutter
- Diwali/Navratri/Dussehra association conveyed through color warmth + restraint, not visual noise

---

### PRODUCTION_RECIPE

1. **Base composition**: Center-aligned vertical poster, dark background, three visual zones
2. **Zone 1 (Top 20%)**: Aight branding and tagline, small and clear
3. **Zone 2 (Middle 60%)**: Pricing and product hierarchy
   - Left column: `IMAGE` + `₹9`
   - Center spacing
   - Right column: `VIDEO` + `₹99`
   - Unified under umbrella phrase: "AI that works for Indian business"
4. **Zone 3 (Bottom 20%)**: Festive context, subtle urgency, CTA, footer
5. **Apply**: Premium sans-serif throughout; no more than 2–3 font weights; white space discipline

---

### GENERATION_PROMPTS

**Single integrated final prompt:**

```
Create a premium 4:5 vertical promotional poster for Aight, an Indian AI API platform. 
Dark charcoal background. Center-aligned layout with generous whitespace. 

Top section (small): "Aight" wordmark / logo and tagline "Where Indian businesses buy AI" in light sans-serif, ~20pt, off-white.

Middle section (dominant): 
Left side: "IMAGE" in bold sans-serif ~48pt, underneath "₹9" in extra-bold geometric sans-serif ~200pt, warm gold/muted saffron color.
Right side: "VIDEO" in bold sans-serif ~48pt, underneath "₹99" in extra-bold geometric sans-serif ~200pt, same warm gold/saffron.
Subtle vertical dividing line or thin geometric accent between them.
Beneath both: "Generation" in smaller serif or refined sans ~36pt, off-white; OR unified label "AI Media Generation."

Below pricing: Small supporting line in light gray, ~28pt: "AI that works for Indian business" OR "Designed for India."

Bottom section: 
Light festive visual hint—optional thin geometric mandala or corner line pattern in 10–15% opacity, warm gold. 
Soft CTA: "This festive season" (optional, small) + "getaight.ai" in 24pt, light weight, off-white.
Footer line: "One domestic invoice. Spend you can see." or similar brand voice, ~18pt, very light gray.

Mood: Serious technology company, premium infrastructure grade, confident pricing transparency. No discount-flyer energy. Professional, clean, minimal. High-end luxury restrain rather than festive chaos.
```

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Use templated design system (not AI generation):**
- Vector-based poster built in professional design tool (Figma, Adobe InDesign, Illustrator)
- Rationale: Pricing, logo, and precise typographic hierarchy require pixel-perfect control; AI image generation introduces unwanted style drift and OCR risk on critical text

**Elements to build deterministically:**
- Aight logo (source from brand files if available; if not, use text-based wordmark)
- All typography (font selection, sizing, kerning, leading)
- Geometric dividers, spacing, background color
- Festive pattern/motif (custom vector or minimal stock graphic, positioned and opacity-controlled precisely)

---

### AUDIO_AND_EDIT

**Not applicable.** This is a static poster. No audio or video editing.

---

### FAILURE_PREVENTION

| Failure Mode | Prevention |
|---|---|
| Pricing gets lost in visual noise | Typography does 90% of work; pricing is largest element; dark background isolates prices |
| Looks like discount flyer, not infrastructure brand | Whitespace discipline, no exclamation marks, one color accent only, professional sans-serif, restraint on festive signals |
| Pricing not immediately readable at mobile distance | ₹9 and ₹99 occupy ~25% of poster height; geometric sans-serif chosen for clarity; no serif confusion on numbers |
| Festive signal overwhelms professionalism | Festive visual = <15% opacity, edge-positioned, geometric only, no illustration |
| GST/billing confusion | Include small line like "One domestic invoice" or "Spend you can see"—reinforces Aight brand voice |
| Call-to-action unclear | Use "getaight.ai" prominently at bottom; optional WhatsApp or "Talk to us" secondary |
| Font kerning/spacing errors on prices | Use production design tool (Figga/InDesign), not AI; manually kern if needed |
| Layout breaks on print or rescale | Build at 2160×2700, test at 1080×1350 and larger; use relative spacing units |

---

### HARD_CONSTRAINT_CHECK

✅ **One poster only** → Delivered as single 4:5 asset  
✅ **Pricing immediately understandable** → ₹9 and ₹99 dominate visual center, largest elements  
✅ **Serious AI infrastructure company feel** → Professional typography, whitespace, minimal decoration, no retail language  
✅ **Typography and hierarchy do most work** → Minimal imagery, design is type-forward  
✅ **Festive season relevance** → Subtle warm-tone accent, optional light geometric motif, "This festive season" optional callout  
✅ **4:5 format** → Vertical poster optimized for mobile/social/print distribution  
✅ **Used only getaight.ai for product/brand info** → All brand voice, product info, tagline sourced from website  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Website used:** https://getaight.ai (frozen snapshot)

**Information extracted and applied:**
- Brand tagline: *"Where Indian businesses buy AI"*
- Core brand values: Transparency, domestic GST invoice, prepaid rupees, "Spend you can see"
- Product mention: Image and voice models ("Image: A curated set")
- Brand voice: Professional, founder-led, honest about control and ROI
- Target audience: Indian businesses (production AI teams, founders, product leaders)
- Positioning: Not a discount play; infrastructure quality with fair pricing and hands-on support

**Specific phrases/tonality borrowed:**
- "Spend you can see. Rupees that behave." → Informs "One domestic invoice" supporting line
- No mention of video pricing on live site, but customer specified ₹99 video; accepted as valid commercial proposition for this festive promotion

---

**END PRODUCTION PACKAGE**

## VISUAL_SYSTEM
**Color Palette:**
- **Primary background**: Deep charcoal or near-black (professional, infrastructure-grade)
- **Pricing highlight**: Warm gold or muted saffron accent (festive restraint, no neon)
- **Text**: Off-white/cream for maximum legibility
- **Accent**: Single secondary color (perhaps a muted deep green or rust) for product descriptor blocks

**Typography:**
- **Pricing numbers** (`₹9`, `₹99`): XL geometric sans-serif, bold weight; approx. 180–240pt
- **Product labels** (`Image`, `Video`, `Generation`): Clean sans-serif, 48–64pt, medium weight
- **Body/supporting text**: 28–36pt, light-to-regular weight, generous line spacing for air
- **Tagline/footer**: 20–24pt, light weight

**Spatial Layout:**
- Centered vertical axis; symmetrical balance
- Large whitespace above and below pricing; breathing room is part of the premium signal
- Product labels flanking pricing with subtle dividing lines or geometric shapes (icons optional)
- Minimal decorative elements; geometric shapes only if they enhance clarity

**Festive Visual Signal:**
- One optional subtle geometric/pattern element (e.g., simplified mandala edge motif, thin line work, corner details) in 10–15% opacity, positioned at edges
- No illustration, no clutter
- Diwali/Navratri/Dussehra association conveyed through color warmth + restraint, not visual noise

---

### PRODUCTION_RECIPE

1. **Base composition**: Center-aligned vertical poster, dark background, three visual zones
2. **Zone 1 (Top 20%)**: Aight branding and tagline, small and clear
3. **Zone 2 (Middle 60%)**: Pricing and product hierarchy
   - Left column: `IMAGE` + `₹9`
   - Center spacing
   - Right column: `VIDEO` + `₹99`
   - Unified under umbrella phrase: "AI that works for Indian business"
4. **Zone 3 (Bottom 20%)**: Festive context, subtle urgency, CTA, footer
5. **Apply**: Premium sans-serif throughout; no more than 2–3 font weights; white space discipline

---

### GENERATION_PROMPTS

**Single integrated final prompt:**

```
Create a premium 4:5 vertical promotional poster for Aight, an Indian AI API platform. 
Dark charcoal background. Center-aligned layout with generous whitespace. 

Top section (small): "Aight" wordmark / logo and tagline "Where Indian businesses buy AI" in light sans-serif, ~20pt, off-white.

Middle section (dominant): 
Left side: "IMAGE" in bold sans-serif ~48pt, underneath "₹9" in extra-bold geometric sans-serif ~200pt, warm gold/muted saffron color.
Right side: "VIDEO" in bold sans-serif ~48pt, underneath "₹99" in extra-bold geometric sans-serif ~200pt, same warm gold/saffron.
Subtle vertical dividing line or thin geometric accent between them.
Beneath both: "Generation" in smaller serif or refined sans ~36pt, off-white; OR unified label "AI Media Generation."

Below pricing: Small supporting line in light gray, ~28pt: "AI that works for Indian business" OR "Designed for India."

Bottom section: 
Light festive visual hint—optional thin geometric mandala or corner line pattern in 10–15% opacity, warm gold. 
Soft CTA: "This festive season" (optional, small) + "getaight.ai" in 24pt, light weight, off-white.
Footer line: "One domestic invoice. Spend you can see." or similar brand voice, ~18pt, very light gray.

Mood: Serious technology company, premium infrastructure grade, confident pricing transparency. No discount-flyer energy. Professional, clean, minimal. High-end luxury restrain rather than festive chaos.
```

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Use templated design system (not AI generation):**
- Vector-based poster built in professional design tool (Figma, Adobe InDesign, Illustrator)
- Rationale: Pricing, logo, and precise typographic hierarchy require pixel-perfect control; AI image generation introduces unwanted style drift and OCR risk on critical text

**Elements to build deterministically:**
- Aight logo (source from brand files if available; if not, use text-based wordmark)
- All typography (font selection, sizing, kerning, leading)
- Geometric dividers, spacing, background color
- Festive pattern/motif (custom vector or minimal stock graphic, positioned and opacity-controlled precisely)

---

### AUDIO_AND_EDIT

**Not applicable.** This is a static poster. No audio or video editing.

---

### FAILURE_PREVENTION

| Failure Mode | Prevention |
|---|---|
| Pricing gets lost in visual noise | Typography does 90% of work; pricing is largest element; dark background isolates prices |
| Looks like discount flyer, not infrastructure brand | Whitespace discipline, no exclamation marks, one color accent only, professional sans-serif, restraint on festive signals |
| Pricing not immediately readable at mobile distance | ₹9 and ₹99 occupy ~25% of poster height; geometric sans-serif chosen for clarity; no serif confusion on numbers |
| Festive signal overwhelms professionalism | Festive visual = <15% opacity, edge-positioned, geometric only, no illustration |
| GST/billing confusion | Include small line like "One domestic invoice" or "Spend you can see"—reinforces Aight brand voice |
| Call-to-action unclear | Use "getaight.ai" prominently at bottom; optional WhatsApp or "Talk to us" secondary |
| Font kerning/spacing errors on prices | Use production design tool (Figga/InDesign), not AI; manually kern if needed |
| Layout breaks on print or rescale | Build at 2160×2700, test at 1080×1350 and larger; use relative spacing units |

---

### HARD_CONSTRAINT_CHECK

✅ **One poster only** → Delivered as single 4:5 asset  
✅ **Pricing immediately understandable** → ₹9 and ₹99 dominate visual center, largest elements  
✅ **Serious AI infrastructure company feel** → Professional typography, whitespace, minimal decoration, no retail language  
✅ **Typography and hierarchy do most work** → Minimal imagery, design is type-forward  
✅ **Festive season relevance** → Subtle warm-tone accent, optional light geometric motif, "This festive season" optional callout  
✅ **4:5 format** → Vertical poster optimized for mobile/social/print distribution  
✅ **Used only getaight.ai for product/brand info** → All brand voice, product info, tagline sourced from website  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Website used:** https://getaight.ai (frozen snapshot)

**Information extracted and applied:**
- Brand tagline: *"Where Indian businesses buy AI"*
- Core brand values: Transparency, domestic GST invoice, prepaid rupees, "Spend you can see"
- Product mention: Image and voice models ("Image: A curated set")
- Brand voice: Professional, founder-led, honest about control and ROI
- Target audience: Indian businesses (production AI teams, founders, product leaders)
- Positioning: Not a discount play; infrastructure quality with fair pricing and hands-on support

**Specific phrases/tonality borrowed:**
- "Spend you can see. Rupees that behave." → Informs "One domestic invoice" supporting line
- No mention of video pricing on live site, but customer specified ₹99 video; accepted as valid commercial proposition for this festive promotion

---

**END PRODUCTION PACKAGE**

## PRODUCTION_RECIPE
1. **Base composition**: Center-aligned vertical poster, dark background, three visual zones
2. **Zone 1 (Top 20%)**: Aight branding and tagline, small and clear
3. **Zone 2 (Middle 60%)**: Pricing and product hierarchy
   - Left column: `IMAGE` + `₹9`
   - Center spacing
   - Right column: `VIDEO` + `₹99`
   - Unified under umbrella phrase: "AI that works for Indian business"
4. **Zone 3 (Bottom 20%)**: Festive context, subtle urgency, CTA, footer
5. **Apply**: Premium sans-serif throughout; no more than 2–3 font weights; white space discipline

---

### GENERATION_PROMPTS

**Single integrated final prompt:**

```
Create a premium 4:5 vertical promotional poster for Aight, an Indian AI API platform. 
Dark charcoal background. Center-aligned layout with generous whitespace. 

Top section (small): "Aight" wordmark / logo and tagline "Where Indian businesses buy AI" in light sans-serif, ~20pt, off-white.

Middle section (dominant): 
Left side: "IMAGE" in bold sans-serif ~48pt, underneath "₹9" in extra-bold geometric sans-serif ~200pt, warm gold/muted saffron color.
Right side: "VIDEO" in bold sans-serif ~48pt, underneath "₹99" in extra-bold geometric sans-serif ~200pt, same warm gold/saffron.
Subtle vertical dividing line or thin geometric accent between them.
Beneath both: "Generation" in smaller serif or refined sans ~36pt, off-white; OR unified label "AI Media Generation."

Below pricing: Small supporting line in light gray, ~28pt: "AI that works for Indian business" OR "Designed for India."

Bottom section: 
Light festive visual hint—optional thin geometric mandala or corner line pattern in 10–15% opacity, warm gold. 
Soft CTA: "This festive season" (optional, small) + "getaight.ai" in 24pt, light weight, off-white.
Footer line: "One domestic invoice. Spend you can see." or similar brand voice, ~18pt, very light gray.

Mood: Serious technology company, premium infrastructure grade, confident pricing transparency. No discount-flyer energy. Professional, clean, minimal. High-end luxury restrain rather than festive chaos.
```

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Use templated design system (not AI generation):**
- Vector-based poster built in professional design tool (Figma, Adobe InDesign, Illustrator)
- Rationale: Pricing, logo, and precise typographic hierarchy require pixel-perfect control; AI image generation introduces unwanted style drift and OCR risk on critical text

**Elements to build deterministically:**
- Aight logo (source from brand files if available; if not, use text-based wordmark)
- All typography (font selection, sizing, kerning, leading)
- Geometric dividers, spacing, background color
- Festive pattern/motif (custom vector or minimal stock graphic, positioned and opacity-controlled precisely)

---

### AUDIO_AND_EDIT

**Not applicable.** This is a static poster. No audio or video editing.

---

### FAILURE_PREVENTION

| Failure Mode | Prevention |
|---|---|
| Pricing gets lost in visual noise | Typography does 90% of work; pricing is largest element; dark background isolates prices |
| Looks like discount flyer, not infrastructure brand | Whitespace discipline, no exclamation marks, one color accent only, professional sans-serif, restraint on festive signals |
| Pricing not immediately readable at mobile distance | ₹9 and ₹99 occupy ~25% of poster height; geometric sans-serif chosen for clarity; no serif confusion on numbers |
| Festive signal overwhelms professionalism | Festive visual = <15% opacity, edge-positioned, geometric only, no illustration |
| GST/billing confusion | Include small line like "One domestic invoice" or "Spend you can see"—reinforces Aight brand voice |
| Call-to-action unclear | Use "getaight.ai" prominently at bottom; optional WhatsApp or "Talk to us" secondary |
| Font kerning/spacing errors on prices | Use production design tool (Figga/InDesign), not AI; manually kern if needed |
| Layout breaks on print or rescale | Build at 2160×2700, test at 1080×1350 and larger; use relative spacing units |

---

### HARD_CONSTRAINT_CHECK

✅ **One poster only** → Delivered as single 4:5 asset  
✅ **Pricing immediately understandable** → ₹9 and ₹99 dominate visual center, largest elements  
✅ **Serious AI infrastructure company feel** → Professional typography, whitespace, minimal decoration, no retail language  
✅ **Typography and hierarchy do most work** → Minimal imagery, design is type-forward  
✅ **Festive season relevance** → Subtle warm-tone accent, optional light geometric motif, "This festive season" optional callout  
✅ **4:5 format** → Vertical poster optimized for mobile/social/print distribution  
✅ **Used only getaight.ai for product/brand info** → All brand voice, product info, tagline sourced from website  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Website used:** https://getaight.ai (frozen snapshot)

**Information extracted and applied:**
- Brand tagline: *"Where Indian businesses buy AI"*
- Core brand values: Transparency, domestic GST invoice, prepaid rupees, "Spend you can see"
- Product mention: Image and voice models ("Image: A curated set")
- Brand voice: Professional, founder-led, honest about control and ROI
- Target audience: Indian businesses (production AI teams, founders, product leaders)
- Positioning: Not a discount play; infrastructure quality with fair pricing and hands-on support

**Specific phrases/tonality borrowed:**
- "Spend you can see. Rupees that behave." → Informs "One domestic invoice" supporting line
- No mention of video pricing on live site, but customer specified ₹99 video; accepted as valid commercial proposition for this festive promotion

---

**END PRODUCTION PACKAGE**

## GENERATION_PROMPTS
**Single integrated final prompt:**

```
Create a premium 4:5 vertical promotional poster for Aight, an Indian AI API platform. 
Dark charcoal background. Center-aligned layout with generous whitespace. 

Top section (small): "Aight" wordmark / logo and tagline "Where Indian businesses buy AI" in light sans-serif, ~20pt, off-white.

Middle section (dominant): 
Left side: "IMAGE" in bold sans-serif ~48pt, underneath "₹9" in extra-bold geometric sans-serif ~200pt, warm gold/muted saffron color.
Right side: "VIDEO" in bold sans-serif ~48pt, underneath "₹99" in extra-bold geometric sans-serif ~200pt, same warm gold/saffron.
Subtle vertical dividing line or thin geometric accent between them.
Beneath both: "Generation" in smaller serif or refined sans ~36pt, off-white; OR unified label "AI Media Generation."

Below pricing: Small supporting line in light gray, ~28pt: "AI that works for Indian business" OR "Designed for India."

Bottom section: 
Light festive visual hint—optional thin geometric mandala or corner line pattern in 10–15% opacity, warm gold. 
Soft CTA: "This festive season" (optional, small) + "getaight.ai" in 24pt, light weight, off-white.
Footer line: "One domestic invoice. Spend you can see." or similar brand voice, ~18pt, very light gray.

Mood: Serious technology company, premium infrastructure grade, confident pricing transparency. No discount-flyer energy. Professional, clean, minimal. High-end luxury restrain rather than festive chaos.
```

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Use templated design system (not AI generation):**
- Vector-based poster built in professional design tool (Figma, Adobe InDesign, Illustrator)
- Rationale: Pricing, logo, and precise typographic hierarchy require pixel-perfect control; AI image generation introduces unwanted style drift and OCR risk on critical text

**Elements to build deterministically:**
- Aight logo (source from brand files if available; if not, use text-based wordmark)
- All typography (font selection, sizing, kerning, leading)
- Geometric dividers, spacing, background color
- Festive pattern/motif (custom vector or minimal stock graphic, positioned and opacity-controlled precisely)

---

### AUDIO_AND_EDIT

**Not applicable.** This is a static poster. No audio or video editing.

---

### FAILURE_PREVENTION

| Failure Mode | Prevention |
|---|---|
| Pricing gets lost in visual noise | Typography does 90% of work; pricing is largest element; dark background isolates prices |
| Looks like discount flyer, not infrastructure brand | Whitespace discipline, no exclamation marks, one color accent only, professional sans-serif, restraint on festive signals |
| Pricing not immediately readable at mobile distance | ₹9 and ₹99 occupy ~25% of poster height; geometric sans-serif chosen for clarity; no serif confusion on numbers |
| Festive signal overwhelms professionalism | Festive visual = <15% opacity, edge-positioned, geometric only, no illustration |
| GST/billing confusion | Include small line like "One domestic invoice" or "Spend you can see"—reinforces Aight brand voice |
| Call-to-action unclear | Use "getaight.ai" prominently at bottom; optional WhatsApp or "Talk to us" secondary |
| Font kerning/spacing errors on prices | Use production design tool (Figga/InDesign), not AI; manually kern if needed |
| Layout breaks on print or rescale | Build at 2160×2700, test at 1080×1350 and larger; use relative spacing units |

---

### HARD_CONSTRAINT_CHECK

✅ **One poster only** → Delivered as single 4:5 asset  
✅ **Pricing immediately understandable** → ₹9 and ₹99 dominate visual center, largest elements  
✅ **Serious AI infrastructure company feel** → Professional typography, whitespace, minimal decoration, no retail language  
✅ **Typography and hierarchy do most work** → Minimal imagery, design is type-forward  
✅ **Festive season relevance** → Subtle warm-tone accent, optional light geometric motif, "This festive season" optional callout  
✅ **4:5 format** → Vertical poster optimized for mobile/social/print distribution  
✅ **Used only getaight.ai for product/brand info** → All brand voice, product info, tagline sourced from website  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Website used:** https://getaight.ai (frozen snapshot)

**Information extracted and applied:**
- Brand tagline: *"Where Indian businesses buy AI"*
- Core brand values: Transparency, domestic GST invoice, prepaid rupees, "Spend you can see"
- Product mention: Image and voice models ("Image: A curated set")
- Brand voice: Professional, founder-led, honest about control and ROI
- Target audience: Indian businesses (production AI teams, founders, product leaders)
- Positioning: Not a discount play; infrastructure quality with fair pricing and hands-on support

**Specific phrases/tonality borrowed:**
- "Spend you can see. Rupees that behave." → Informs "One domestic invoice" supporting line
- No mention of video pricing on live site, but customer specified ₹99 video; accepted as valid commercial proposition for this festive promotion

---

**END PRODUCTION PACKAGE**

## DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS
**Use templated design system (not AI generation):**
- Vector-based poster built in professional design tool (Figma, Adobe InDesign, Illustrator)
- Rationale: Pricing, logo, and precise typographic hierarchy require pixel-perfect control; AI image generation introduces unwanted style drift and OCR risk on critical text

**Elements to build deterministically:**
- Aight logo (source from brand files if available; if not, use text-based wordmark)
- All typography (font selection, sizing, kerning, leading)
- Geometric dividers, spacing, background color
- Festive pattern/motif (custom vector or minimal stock graphic, positioned and opacity-controlled precisely)

---

### AUDIO_AND_EDIT

**Not applicable.** This is a static poster. No audio or video editing.

---

### FAILURE_PREVENTION

| Failure Mode | Prevention |
|---|---|
| Pricing gets lost in visual noise | Typography does 90% of work; pricing is largest element; dark background isolates prices |
| Looks like discount flyer, not infrastructure brand | Whitespace discipline, no exclamation marks, one color accent only, professional sans-serif, restraint on festive signals |
| Pricing not immediately readable at mobile distance | ₹9 and ₹99 occupy ~25% of poster height; geometric sans-serif chosen for clarity; no serif confusion on numbers |
| Festive signal overwhelms professionalism | Festive visual = <15% opacity, edge-positioned, geometric only, no illustration |
| GST/billing confusion | Include small line like "One domestic invoice" or "Spend you can see"—reinforces Aight brand voice |
| Call-to-action unclear | Use "getaight.ai" prominently at bottom; optional WhatsApp or "Talk to us" secondary |
| Font kerning/spacing errors on prices | Use production design tool (Figga/InDesign), not AI; manually kern if needed |
| Layout breaks on print or rescale | Build at 2160×2700, test at 1080×1350 and larger; use relative spacing units |

---

### HARD_CONSTRAINT_CHECK

✅ **One poster only** → Delivered as single 4:5 asset  
✅ **Pricing immediately understandable** → ₹9 and ₹99 dominate visual center, largest elements  
✅ **Serious AI infrastructure company feel** → Professional typography, whitespace, minimal decoration, no retail language  
✅ **Typography and hierarchy do most work** → Minimal imagery, design is type-forward  
✅ **Festive season relevance** → Subtle warm-tone accent, optional light geometric motif, "This festive season" optional callout  
✅ **4:5 format** → Vertical poster optimized for mobile/social/print distribution  
✅ **Used only getaight.ai for product/brand info** → All brand voice, product info, tagline sourced from website  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Website used:** https://getaight.ai (frozen snapshot)

**Information extracted and applied:**
- Brand tagline: *"Where Indian businesses buy AI"*
- Core brand values: Transparency, domestic GST invoice, prepaid rupees, "Spend you can see"
- Product mention: Image and voice models ("Image: A curated set")
- Brand voice: Professional, founder-led, honest about control and ROI
- Target audience: Indian businesses (production AI teams, founders, product leaders)
- Positioning: Not a discount play; infrastructure quality with fair pricing and hands-on support

**Specific phrases/tonality borrowed:**
- "Spend you can see. Rupees that behave." → Informs "One domestic invoice" supporting line
- No mention of video pricing on live site, but customer specified ₹99 video; accepted as valid commercial proposition for this festive promotion

---

**END PRODUCTION PACKAGE**

## FAILURE_PREVENTION
| Failure Mode | Prevention |
|---|---|
| Pricing gets lost in visual noise | Typography does 90% of work; pricing is largest element; dark background isolates prices |
| Looks like discount flyer, not infrastructure brand | Whitespace discipline, no exclamation marks, one color accent only, professional sans-serif, restraint on festive signals |
| Pricing not immediately readable at mobile distance | ₹9 and ₹99 occupy ~25% of poster height; geometric sans-serif chosen for clarity; no serif confusion on numbers |
| Festive signal overwhelms professionalism | Festive visual = <15% opacity, edge-positioned, geometric only, no illustration |
| GST/billing confusion | Include small line like "One domestic invoice" or "Spend you can see"—reinforces Aight brand voice |
| Call-to-action unclear | Use "getaight.ai" prominently at bottom; optional WhatsApp or "Talk to us" secondary |
| Font kerning/spacing errors on prices | Use production design tool (Figga/InDesign), not AI; manually kern if needed |
| Layout breaks on print or rescale | Build at 2160×2700, test at 1080×1350 and larger; use relative spacing units |

---

### HARD_CONSTRAINT_CHECK

✅ **One poster only** → Delivered as single 4:5 asset  
✅ **Pricing immediately understandable** → ₹9 and ₹99 dominate visual center, largest elements  
✅ **Serious AI infrastructure company feel** → Professional typography, whitespace, minimal decoration, no retail language  
✅ **Typography and hierarchy do most work** → Minimal imagery, design is type-forward  
✅ **Festive season relevance** → Subtle warm-tone accent, optional light geometric motif, "This festive season" optional callout  
✅ **4:5 format** → Vertical poster optimized for mobile/social/print distribution  
✅ **Used only getaight.ai for product/brand info** → All brand voice, product info, tagline sourced from website  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Website used:** https://getaight.ai (frozen snapshot)

**Information extracted and applied:**
- Brand tagline: *"Where Indian businesses buy AI"*
- Core brand values: Transparency, domestic GST invoice, prepaid rupees, "Spend you can see"
- Product mention: Image and voice models ("Image: A curated set")
- Brand voice: Professional, founder-led, honest about control and ROI
- Target audience: Indian businesses (production AI teams, founders, product leaders)
- Positioning: Not a discount play; infrastructure quality with fair pricing and hands-on support

**Specific phrases/tonality borrowed:**
- "Spend you can see. Rupees that behave." → Informs "One domestic invoice" supporting line
- No mention of video pricing on live site, but customer specified ₹99 video; accepted as valid commercial proposition for this festive promotion

---

**END PRODUCTION PACKAGE**

## HARD_CONSTRAINT_CHECK
✅ **One poster only** → Delivered as single 4:5 asset  
✅ **Pricing immediately understandable** → ₹9 and ₹99 dominate visual center, largest elements  
✅ **Serious AI infrastructure company feel** → Professional typography, whitespace, minimal decoration, no retail language  
✅ **Typography and hierarchy do most work** → Minimal imagery, design is type-forward  
✅ **Festive season relevance** → Subtle warm-tone accent, optional light geometric motif, "This festive season" optional callout  
✅ **4:5 format** → Vertical poster optimized for mobile/social/print distribution  
✅ **Used only getaight.ai for product/brand info** → All brand voice, product info, tagline sourced from website  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Website used:** https://getaight.ai (frozen snapshot)

**Information extracted and applied:**
- Brand tagline: *"Where Indian businesses buy AI"*
- Core brand values: Transparency, domestic GST invoice, prepaid rupees, "Spend you can see"
- Product mention: Image and voice models ("Image: A curated set")
- Brand voice: Professional, founder-led, honest about control and ROI
- Target audience: Indian businesses (production AI teams, founders, product leaders)
- Positioning: Not a discount play; infrastructure quality with fair pricing and hands-on support

**Specific phrases/tonality borrowed:**
- "Spend you can see. Rupees that behave." → Informs "One domestic invoice" supporting line
- No mention of video pricing on live site, but customer specified ₹99 video; accepted as valid commercial proposition for this festive promotion

---

**END PRODUCTION PACKAGE**

## GENERATE I03
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I04 — B03

Source key: E037-haiku-no-canon-B03-R1
Use frozen brief B03 from the top of this file.



## GENERATE I04
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I05 — B03

Source key: E037-haiku-no-canon-B03-R2
Use frozen brief B03 from the top of this file.



## GENERATE I05
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I06 — B03

Source key: E037-haiku-no-canon-B03-R3
Use frozen brief B03 from the top of this file.

## DELIVERABLE
Single premium 4:5 vertical advertising image (portrait orientation) for digital/social platforms.

---

## OBJECTIVE_INTERPRETATION
Create one hero-focused product image that positions a mosambi sparkling drink as sophisticated and contemporary, appealing to urban Indian adults aged 22–35. The image must authenticate the product through visible mosambi fruit and carbonation, feel refined (not mass-market), and avoid decorative "Indianness" while retaining cultural rootedness. The product must be unmistakable and dominate the frame.

---

## CORE_CREATIVE_IDEA
**Clean Product Hero + Subtle Authenticity**

A premium glass of mosambi sparkling water in a contemporary setting, lit to showcase carbonation, with one halved mosambi fruit positioned naturally nearby as a visual claim of origin. The composition is minimalist and modern—product forward, context restrained. No bottle clutter, no lifestyle figures, no patterns or motifs. The drink's natural lime-green translucency and visible bubbles are the focal point.

---

## MESSAGE_AND_INFORMATION_HIERARCHY
1. **Primary**: The drink itself—clear, fresh, sparkling, premium presentation
2. **Secondary**: Mosambi as the source ingredient (visual proof via halved fruit)
3. **Tertiary**: Contemporary, controlled environment (suggests quality/care)
4. **Avoid**: Cheapness, overcrowding, cultural cliché, ambiguity about what the product is

---

## VISUAL_SYSTEM
**Color Palette**:
- Drink: Clear with natural lime-green translucency, visible carbonation
- Background: Soft neutral (off-white, pale grey, or subtle warm beige)
- Mosambi fruit: Natural pale yellow-green
- Glassware: Clear or very pale neutral
- Accents: Minimal—perhaps a single ice cube or natural condensation

**Composition**:
- 4:5 vertical frame
- Product glass positioned slightly off-center, high enough to command the upper 60% of frame
- Mosambi half(s) positioned lower-left or lower-right, in shallow focus or natural shadow
- Negative space: Generous, uncluttered, contemporary
- Depth: Shallow depth of field to isolate product, soft blur on background

**Lighting**:
- Key light: Bright, slightly warm, hitting the glass to show sparkle and translucency
- No harsh shadows; soft, diffused
- Carbonation bubbles must be visible and luminous
- Condensation on glass optional but adds tactile premium feel

**Typography/Branding**:
- No text in the image unless product label is minimal/readable on glass—keep unobtrusive
- Focus is visual, not textual

**Aesthetic Reference**:
- Minimalist beverage advertising (contemporary international premium drinks)
- Clean, modern, not nostalgic
- Editorial/gallery-quality photography feel, not mass-market soda-aisle aesthetic

---

## PRODUCTION_RECIPE
1. **Setup**:
   - Clean, neutral background surface (matte white or warm grey wall, or minimal lifestyle table)
   - Bright, diffused key light from front-left
   - Clear, cylindrical or softly tapered glass (approximately 350–400ml capacity)
   - Two mosambi fruits (at least one halved to show interior)
   - Optional: 2–3 ice cubes, water droplets on glass for condensation

2. **Preparation**:
   - Freshly prepared mosambi sparkling water (pale lime-green, visible bubbles)
   - Chill glass; pour drink immediately before shoot to maximize bubble visibility
   - Position halved mosambi nearby, slightly out of focus or in shadow

3. **Framing**:
   - Vertical 4:5 ratio lock
   - Glass occupies center-to-upper frame
   - Rule of thirds: product slightly off-center vertically
   - Fruit in lower third, soft or ambient focus
   - Headroom: minimal above glass rim

4. **Post-Production**:
   - Enhance natural carbonation bubble visibility (subtle, not artificial)
   - Warm/neutral color correction to maintain natural lime translucency
   - Slight texture and tone refinement for premium editorial feel
   - No filters; natural, refined aesthetic

---

## GENERATION_PROMPTS
**SINGLE FINAL GENERATION PROMPT:**

> A premium 4:5 vertical product photograph of a tall clear glass filled with pale lime-green sparkling mosambi juice, shot against a soft neutral warm-grey background. The glass is positioned slightly off-center in the upper-middle frame, brightly lit from the front-left to show visible carbonation bubbles luminous within the drink. Condensation beads on the outside of the glass. In the lower frame, slightly out of focus, sits a halved fresh mosambi fruit (sweet lime) showing the pale yellow interior. Minimal negative space. Clean, contemporary, editorial aesthetic—no text, no patterns, no decorative elements. Shot with shallow depth of field. The overall mood is fresh, refined, and sophisticated, evoking premium contemporary beverage advertising. No clichéd visual references; purely modern and ingredient-focused. High-resolution, professional product photography quality.

---

## DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS
**Should be deterministic (photographic/3D render, not AI-generated) for optimal premium quality:**
- Actual product photography with real mosambi fruit, sparkling water, and glass
- Real carbonation bubbles visible and captured in-camera
- Real condensation and light refraction through liquid

**Rationale**: AI generation at this premium level risks:
- Inconsistent bubble patterns or unrealistic carbonation
- Uncanny liquid rendering
- Fruit texture/dimension feel inauthentic
- Loss of professional beverage-advertising credibility

**If AI generation is mandatory**: Use prompt above but request high-fidelity photorealism, specify "high-end commercial beverage photography," and request multiple generations to select highest product-fidelity result. Post-processing to enhance bubble/liquid realism will be required.

---

## FAILURE_PREVENTION
**What must NOT happen:**
1. ✗ Product unclear or secondary to background/styling
2. ✗ Drink looks opaque, flat, or unappealing (must read as fresh and carbonated)
3. ✗ Mosambi presented as decoration—must feel like authentic ingredient evidence
4. ✗ Cheap soda-aisle aesthetic (plastic bottles, artificial colors, overstylized props)
5. ✗ Clichéd Indian visual language (patterns, gold accents, traditional motifs, warm spice tones)
6. ✗ Overcrowded frame—must feel curated and spacious
7. ✗ Unclear product identity—must unmistakably read as a premium sparkling drink, not juice or soda
8. ✗ Mosambi fruit looks old or bruised—must be fresh, vibrant, natural
9. ✗ Lighting that flattens the drink or hides carbonation
10. ✗ Any visible branding, celebrity, or text clutter

**Quality gates before final**:
- Bubble visibility and realism check
- Mosambi color authenticity (pale yellow-green, not orange or artificial lime)
- Glass clarity and condensation check
- Background neutrality check (not distracting, not overstylized)
- 4:5 ratio confirmation
- Premium aesthetic consensus (would this appear in high-end lifestyle or food publication?)

---

## HARD_CONSTRAINT_CHECK
✓ Premium 4:5 advertising image: **YES**  
✓ Mosambi sparkling drink product: **YES—unmistakable hero**  
✓ Urban 22–35 demographic targeting: **YES—minimalist, contemporary styling**  
✓ Refreshing + sophisticated + contemporary: **YES—clean, bright, modern aesthetic**  
✓ Retains mosambi familiarity: **YES—fruit visible and prominent**  
✓ Avoids clichéd Indian visual shorthand: **YES—no patterns, motifs, or decorative Indianness**  
✓ Avoids cheap soft-drink aesthetic: **YES—premium glassware, editorial lighting, restrained styling**  
✓ Product is unmistakable hero: **YES—positioned upper-center, well-lit, dominant**  
✓ No celebrity: **YES—product-only focus**  
✓ No external website references: **YES**  

---

## GENERATE I06
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I07 — B06

Source key: E037-haiku-no-canon-B06-R1
Use frozen brief B06 from the top of this file.

## DELIVERABLE
Premium 4:5 e-commerce hero image for Aster Meridian 38 mechanical watch.

## OBJECTIVE_INTERPRETATION
Produce a single, commercially viable product hero image that showcases dial artistry, material quality, and craftsmanship integrity. The image must clearly communicate the watch as a desirable precision instrument while remaining suitable for a luxury product page. All product specifications are fixed and non-negotiable.

## CORE_CREATIVE_IDEA
Three-quarter angled close-up of the watch positioned on a neutral, refined surface. Composition emphasizes the deep blue sunburst dial through controlled directional lighting, reveals case brushing and sapphire crystal clarity, and includes the leather strap as a material counterpoint. Minimal, uncluttered framing centered on the product itself.

## MESSAGE_AND_INFORMATION_HIERARCHY
1. Dial artistry (sunburst depth, silver marker precision, hand design)
2. Material quality (brushed stainless case, sapphire crystal, brown leather)
3. Mechanical refinement (proportional 38mm case, clean dial architecture)
4. Wearability and desirability (strap visibility, proportionate positioning)

## VISUAL_SYSTEM
- **Lighting**: Directional key light at ~45° to emphasize sunburst dial radiance and case brushing; soft fill to show crystal without flare artifacts
- **Angle**: 3/4 view, watch tilted 15–20° from horizontal to show dial face clearly while revealing case side profile and strap
- **Background**: Neutral stone grey or warm off-white, non-reflective matte finish
- **Surface base**: Minimal—slight platform shadow or subtle surface texture, not distracting
- **Color palette**: Blue dial as primary focus; silver accents pop against neutral surround; brown strap provides warmth and visual anchor

## PRODUCTION_RECIPE
1. **Setup**: Watch positioned on low platform angled to camera. Case sits in frame with enough margin for 4:5 crop. Dial faces slightly upward, visible in primary focus.
2. **Lighting**: Single key light creating sunburst glow on dial; secondary softer fill preserving shadow definition on case.
3. **Capture/generation**: Close enough to show hour marker detail and hand geometry; far enough to frame complete watch with breathing room top and bottom (4:5 ratio).
4. **Post-processing**: Minimal—ensure accurate color reproduction of deep blue, silver metals, and brown leather; preserve dial sunburst texture; controlled contrast to enhance crystal clarity without overdoing.

## GENERATION_PROMPTS
**FINAL GENERATION PROMPT:**

"Premium product photograph of a 38mm mechanical watch, Aster Meridian 38, shot in 4:5 portrait aspect ratio. Watch positioned at 3/4 angle on a neutral stone-grey matte surface. The watch displays a deep blue sunburst dial with silver baton hour markers and silver dauphine hands (no date window). Brushed stainless-steel case with domed sapphire crystal catching controlled directional light. Dark brown leather strap visible on right side of frame. Directional key lighting at 45° emphasizes the radial sunburst texture on the dial and the case brushing; soft fill light reveals crystal clarity. Background is neutral, non-reflective, with subtle surface definition. Framing includes complete watch with balanced negative space above and below. Sharp focus across dial and case. Professional e-commerce product photography aesthetic. Color-accurate representation of blue dial, silver metals, brushed steel, and brown leather."

## DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS
- Product specifications are fixed (38mm, brushed stainless, deep blue sunburst, silver baton markers, silver dauphine hands, no date, domed sapphire, brown leather strap)
- Case geometry, hand design, dial layout must not be altered
- 4:5 aspect ratio is fixed
- Lighting direction and intensity can be controlled post-generation if needed
- Color correction may be applied to ensure accurate blue, silver, and brown tones

## FAILURE_PREVENTION
- **Watch accuracy check**: Verify all product details match specification—case size, dial color, marker style, hand design, strap color—before approving image.
- **Dial readability**: Ensure markers and hands are clearly visible and distinguishable; sunburst pattern is apparent but not overwhelming.
- **Crystal clarity**: Sapphire reflection should be subtle and elegant, not a harsh glare.
- **Strap visibility**: Brown leather should photograph as dark brown, not black or tan; texture should be visible but not distracting.
- **Aspect ratio verification**: Confirm output is exactly 4:5 (e.g., 1080×1350px or equivalent).
- **Color accuracy**: Compare blue dial, silver accents, and brushed steel against reference if available; adjust if generation leans too warm, cool, or desaturated.

## HARD_CONSTRAINT_CHECK
- ✓ 4:5 aspect ratio specified and enforced
- ✓ No external websites used
- ✓ All product facts preserved (38mm, brushed stainless, deep blue sunburst, silver baton markers, silver dauphine hands, no date, sapphire, brown leather)
- ✓ Craftsmanship, dial detail, material quality, and desirability all addressed in composition and lighting
- ✓ Commercially suitable for premium product page
- ✓ Avoids generic floating CGI; product is positioned on a surface in a controlled, professional shot

## GENERATE I07
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I08 — B06

Source key: E037-haiku-no-canon-B06-R2
Use frozen brief B06 from the top of this file.



## GENERATE I08
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I09 — B06

Source key: E037-haiku-no-canon-B06-R3
Use frozen brief B06 from the top of this file.



## GENERATE I09
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---
