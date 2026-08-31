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

# IMAGE JOB I10 — B02

Source key: E037-haiku-full-canon-B02-R1
Use frozen brief B02 from the top of this file.

## DELIVERABLE
Single 4:5 vertical poster (1080×1350px or 2160×2700px for print). Premium promotion for aight's media-generation API (image and video) during Indian festive season, emphasizing price transparency and enterprise-grade positioning.

---

### OBJECTIVE_INTERPRETATION
Announce aight's image and video generation pricing (₹9 and ₹99 respectively) to Indian businesses during festive buying season. Position the offer as serious AI infrastructure, not discount retail. Let pricing be the hero but keep brand authority intact.

---

### CORE_CREATIVE_IDEA
**Silence the numbers. Speak through hierarchy.**

A clean, vertical typographic layout that treats the two prices as structural pillars—not promotional "call-outs." Image generation (₹9) and video generation (₹99) sit at visual/cognitive center, with minimal context around them. No currency symbol inflation, no exclamation marks, no discount language. The pricing is the statement. Brand voice remains institutional, builder-focused, India-native.

---

### MESSAGE_AND_INFORMATION_HIERARCHY

**Tier 1 (Dominant – visual center):**
- The two prices: ₹9 and ₹99
- Matched line-height; neutral sans-serif; identical visual weight

**Tier 2 (Supporting structure):**
- What each price unlocks: "Image" / "Video" (small, above or beside prices)
- Single line of benefit/call: "For Indian builders" or "Now live"

**Tier 3 (Institutional grounding):**
- Brand: "aight" (very small, top or bottom)
- Tagline from website: "Where Indian businesses buy AI" (minimal, gray, bottom)
- URL: getaight.ai (footer, small)

**Tone:** Direct. No hype. No adjectives. Numbers speak for themselves.

---

### VISUAL_SYSTEM

**Color Palette:**
- **Background:** Off-white or very soft warm white (festive but not garish; aligns with enterprise aesthetic)
- **Typography:** Near-black for prices and primary text; mid-gray for tier 2/3 supporting text
- **Accent (optional):** One subtle color from Indian festive palette (deep saffron or deep green) used only in the separator line or logo lockup—reserved, not dominant

**Typography:**
- **Price numbers:** Large, geometric sans-serif (e.g., Inter, Grotesk, or similar—neutral, high-contrast)
  - ₹9: ~120–140px
  - ₹99: ~120–140px
- **Labels ("Image" / "Video"):** ~32–40px, same or lighter weight, positioned directly above/beside
- **Brand and footer text:** ~16–20px, medium or regular weight
- **Line height & spacing:** Generous vertical rhythm; prices separated by 60–100px of white space from brand/footer

**Layout Structure:**
- Vertical: top ¼ negative space → center ½ prices + labels → bottom ¼ brand + footer
- Symmetry or subtle asymmetry (e.g., prices left-aligned, labels right, creating a visual grid without clutter)
- No decorative graphics, icons, or photography
- Single vertical separator line (thin, 1–2px) between image and video pricing areas (optional; improves scannability)

---

### PRODUCTION_RECIPE

1. **Typeface Selection:** Download/license one neutral geometric sans-serif (must support Indian numerals; Unicode for ₹ symbol)
2. **Composition Grid:** 1080×1350px canvas. Divide into thirds vertically. Prices occupy center third.
3. **Color Mixing:** Define off-white background RGB/hex; near-black text RGB/hex; optional accent color (saffron #FF9F43 or forest green #2D5016, desaturated to ~60% saturation for restraint)
4. **Element Placement:**
   - "Image" label @ 480px from top, centered or left-aligned
   - ₹9 price @ 550px from top
   - "Video" label @ 750px from top
   - ₹99 price @ 820px from top
   - "aight" logo/wordmark @ 1150px from top (very small)
   - "Where Indian businesses buy AI" @ 1240px from top
   - "getaight.ai" @ 1300px from top
5. **Refinement:** Kern price numbers for visual balance. Test at 1080×1350 and at print sizes (300dpi for print).

---

### GENERATION_PROMPTS

**Single Executable Final Generation Prompt:**

> Create a minimalist premium promotional poster (4:5 ratio, vertical orientation) for an AI infrastructure company in India. The poster announces pricing for media-generation APIs:
> 
> **Visual hierarchy (top to bottom):**
> - Ample white space at the very top
> - The word "Image" in small, gray sans-serif at top-center
> - Below it, the price "₹9" in very large, bold geometric sans-serif (130pt equivalent), nearly black
> - A thin vertical separator line running between the left and right halves (optional; very subtle)
> - On the right side, the word "Video" in the same small gray sans-serif
> - Below it, "₹99" in the same large bold geometric sans-serif
> - Ample white space in the middle
> - Very bottom: the brand name "aight" in small sans-serif
> - Below that: "Where Indian businesses buy AI" in even smaller gray sans-serif
> - Footer: "getaight.ai" in tiny text
> 
> **Design principles:**
> - Background: soft off-white or warm cream (festive but not bright)
> - No icons, photos, or decorative elements
> - Typography carries 100% of the message
> - Pricing is the visual and conceptual centerpiece
> - Tone: institutional, direct, serious—not a discount retail flyer
> - Grid-based composition with generous negative space
> - Suitable for high-resolution print and digital display
> 
> Do not include promotional language like "Special Offer," "Now Available," or discount framing. Let the prices stand alone as the statement.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Brand logo/wordmark "aight":** Use official aight wordmark from getaight.ai (source: website). If unavailable in frozen snapshot, render as clean sans-serif lowercase "aight" in near-black.
- **Currency symbol (₹):** Render using Unicode U+20B9 or equivalent font glyph; ensure anti-aliasing is clean at large sizes.
- **Tagline text:** "Where Indian businesses buy AI" (exact phrasing from website homepage—mandatory for brand consistency).
- **URL:** "getaight.ai" (exact from website footer).

---

### AUDIO_AND_EDIT

**N/A.** Deliverable is a static poster; no audio, video edit, or animation.

---

### FAILURE_PREVENTION

1. **Price Prominence:** If image-generation price (₹9) is less visually dominant than video (₹99), rebalance by font size or position—both prices must be equally immediate and scannable.
2. **Brand Legibility at Thumbnail:** Shrink mockup to 300px width; verify "aight" and "getaight.ai" remain readable and positioned logically.
3. **Festive Context Check:** Ensure background color/tone evokes festive season without cacophony. Soft warm white + optional deep saffron/green accent is sufficient; avoid neon or overstimulating palettes.
4. **Enterprise Tone Preservation:** Remove any language or graphic flourishes that read as "discount" or "sale." Pricing is announcement, not promotion.
5. **Color Contrast:** Test near-black text on off-white background for WCAG AA compliance (contrast ratio ≥4.5:1). Test small footer text contrast separately.
6. **Print Readiness:** If poster will be printed, export at 300dpi; verify fonts embed or outline correctly; test on physical substrate (stock/finish appropriate for B2B office/event display).

---

### HARD_CONSTRAINT_CHECK

✓ Format: 4:5 vertical poster (executable as 1080×1350px or 2160×2700px print-ready)  
✓ Prices visible and immediately understandable (₹9 for image, ₹99 for video)  
✓ Premium/institutional tone, not retail flyer  
✓ Typography and hierarchy carry the design  
✓ Brand/product information sourced from getaight.ai only  
✓ Indian festive season context acknowledged (warm, clean aesthetic; no assumption of specific festival, but seasonal tone present)  
✓ Single concept, no alternatives  
✓ Production-ready prompts provided  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (primary): Brand positioning ("Where Indian businesses buy AI"), company entity name "aight," official tagline, target audience (Indian businesses), services (image and video generation), URL, founding principles (prepaid rupees, domestic GST, builder-focused, no-hype).

**Canon knowledge:** None consulted. Brand information and positioning constraints sourced entirely from getaight.ai website snapshot.

---

**END PRODUCTION PACKAGE**

## OBJECTIVE_INTERPRETATION
Announce aight's image and video generation pricing (₹9 and ₹99 respectively) to Indian businesses during festive buying season. Position the offer as serious AI infrastructure, not discount retail. Let pricing be the hero but keep brand authority intact.

---

### CORE_CREATIVE_IDEA
**Silence the numbers. Speak through hierarchy.**

A clean, vertical typographic layout that treats the two prices as structural pillars—not promotional "call-outs." Image generation (₹9) and video generation (₹99) sit at visual/cognitive center, with minimal context around them. No currency symbol inflation, no exclamation marks, no discount language. The pricing is the statement. Brand voice remains institutional, builder-focused, India-native.

---

### MESSAGE_AND_INFORMATION_HIERARCHY

**Tier 1 (Dominant – visual center):**
- The two prices: ₹9 and ₹99
- Matched line-height; neutral sans-serif; identical visual weight

**Tier 2 (Supporting structure):**
- What each price unlocks: "Image" / "Video" (small, above or beside prices)
- Single line of benefit/call: "For Indian builders" or "Now live"

**Tier 3 (Institutional grounding):**
- Brand: "aight" (very small, top or bottom)
- Tagline from website: "Where Indian businesses buy AI" (minimal, gray, bottom)
- URL: getaight.ai (footer, small)

**Tone:** Direct. No hype. No adjectives. Numbers speak for themselves.

---

### VISUAL_SYSTEM

**Color Palette:**
- **Background:** Off-white or very soft warm white (festive but not garish; aligns with enterprise aesthetic)
- **Typography:** Near-black for prices and primary text; mid-gray for tier 2/3 supporting text
- **Accent (optional):** One subtle color from Indian festive palette (deep saffron or deep green) used only in the separator line or logo lockup—reserved, not dominant

**Typography:**
- **Price numbers:** Large, geometric sans-serif (e.g., Inter, Grotesk, or similar—neutral, high-contrast)
  - ₹9: ~120–140px
  - ₹99: ~120–140px
- **Labels ("Image" / "Video"):** ~32–40px, same or lighter weight, positioned directly above/beside
- **Brand and footer text:** ~16–20px, medium or regular weight
- **Line height & spacing:** Generous vertical rhythm; prices separated by 60–100px of white space from brand/footer

**Layout Structure:**
- Vertical: top ¼ negative space → center ½ prices + labels → bottom ¼ brand + footer
- Symmetry or subtle asymmetry (e.g., prices left-aligned, labels right, creating a visual grid without clutter)
- No decorative graphics, icons, or photography
- Single vertical separator line (thin, 1–2px) between image and video pricing areas (optional; improves scannability)

---

### PRODUCTION_RECIPE

1. **Typeface Selection:** Download/license one neutral geometric sans-serif (must support Indian numerals; Unicode for ₹ symbol)
2. **Composition Grid:** 1080×1350px canvas. Divide into thirds vertically. Prices occupy center third.
3. **Color Mixing:** Define off-white background RGB/hex; near-black text RGB/hex; optional accent color (saffron #FF9F43 or forest green #2D5016, desaturated to ~60% saturation for restraint)
4. **Element Placement:**
   - "Image" label @ 480px from top, centered or left-aligned
   - ₹9 price @ 550px from top
   - "Video" label @ 750px from top
   - ₹99 price @ 820px from top
   - "aight" logo/wordmark @ 1150px from top (very small)
   - "Where Indian businesses buy AI" @ 1240px from top
   - "getaight.ai" @ 1300px from top
5. **Refinement:** Kern price numbers for visual balance. Test at 1080×1350 and at print sizes (300dpi for print).

---

### GENERATION_PROMPTS

**Single Executable Final Generation Prompt:**

> Create a minimalist premium promotional poster (4:5 ratio, vertical orientation) for an AI infrastructure company in India. The poster announces pricing for media-generation APIs:
> 
> **Visual hierarchy (top to bottom):**
> - Ample white space at the very top
> - The word "Image" in small, gray sans-serif at top-center
> - Below it, the price "₹9" in very large, bold geometric sans-serif (130pt equivalent), nearly black
> - A thin vertical separator line running between the left and right halves (optional; very subtle)
> - On the right side, the word "Video" in the same small gray sans-serif
> - Below it, "₹99" in the same large bold geometric sans-serif
> - Ample white space in the middle
> - Very bottom: the brand name "aight" in small sans-serif
> - Below that: "Where Indian businesses buy AI" in even smaller gray sans-serif
> - Footer: "getaight.ai" in tiny text
> 
> **Design principles:**
> - Background: soft off-white or warm cream (festive but not bright)
> - No icons, photos, or decorative elements
> - Typography carries 100% of the message
> - Pricing is the visual and conceptual centerpiece
> - Tone: institutional, direct, serious—not a discount retail flyer
> - Grid-based composition with generous negative space
> - Suitable for high-resolution print and digital display
> 
> Do not include promotional language like "Special Offer," "Now Available," or discount framing. Let the prices stand alone as the statement.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Brand logo/wordmark "aight":** Use official aight wordmark from getaight.ai (source: website). If unavailable in frozen snapshot, render as clean sans-serif lowercase "aight" in near-black.
- **Currency symbol (₹):** Render using Unicode U+20B9 or equivalent font glyph; ensure anti-aliasing is clean at large sizes.
- **Tagline text:** "Where Indian businesses buy AI" (exact phrasing from website homepage—mandatory for brand consistency).
- **URL:** "getaight.ai" (exact from website footer).

---

### AUDIO_AND_EDIT

**N/A.** Deliverable is a static poster; no audio, video edit, or animation.

---

### FAILURE_PREVENTION

1. **Price Prominence:** If image-generation price (₹9) is less visually dominant than video (₹99), rebalance by font size or position—both prices must be equally immediate and scannable.
2. **Brand Legibility at Thumbnail:** Shrink mockup to 300px width; verify "aight" and "getaight.ai" remain readable and positioned logically.
3. **Festive Context Check:** Ensure background color/tone evokes festive season without cacophony. Soft warm white + optional deep saffron/green accent is sufficient; avoid neon or overstimulating palettes.
4. **Enterprise Tone Preservation:** Remove any language or graphic flourishes that read as "discount" or "sale." Pricing is announcement, not promotion.
5. **Color Contrast:** Test near-black text on off-white background for WCAG AA compliance (contrast ratio ≥4.5:1). Test small footer text contrast separately.
6. **Print Readiness:** If poster will be printed, export at 300dpi; verify fonts embed or outline correctly; test on physical substrate (stock/finish appropriate for B2B office/event display).

---

### HARD_CONSTRAINT_CHECK

✓ Format: 4:5 vertical poster (executable as 1080×1350px or 2160×2700px print-ready)  
✓ Prices visible and immediately understandable (₹9 for image, ₹99 for video)  
✓ Premium/institutional tone, not retail flyer  
✓ Typography and hierarchy carry the design  
✓ Brand/product information sourced from getaight.ai only  
✓ Indian festive season context acknowledged (warm, clean aesthetic; no assumption of specific festival, but seasonal tone present)  
✓ Single concept, no alternatives  
✓ Production-ready prompts provided  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (primary): Brand positioning ("Where Indian businesses buy AI"), company entity name "aight," official tagline, target audience (Indian businesses), services (image and video generation), URL, founding principles (prepaid rupees, domestic GST, builder-focused, no-hype).

**Canon knowledge:** None consulted. Brand information and positioning constraints sourced entirely from getaight.ai website snapshot.

---

**END PRODUCTION PACKAGE**

## CORE_CREATIVE_IDEA
**Silence the numbers. Speak through hierarchy.**

A clean, vertical typographic layout that treats the two prices as structural pillars—not promotional "call-outs." Image generation (₹9) and video generation (₹99) sit at visual/cognitive center, with minimal context around them. No currency symbol inflation, no exclamation marks, no discount language. The pricing is the statement. Brand voice remains institutional, builder-focused, India-native.

---

### MESSAGE_AND_INFORMATION_HIERARCHY

**Tier 1 (Dominant – visual center):**
- The two prices: ₹9 and ₹99
- Matched line-height; neutral sans-serif; identical visual weight

**Tier 2 (Supporting structure):**
- What each price unlocks: "Image" / "Video" (small, above or beside prices)
- Single line of benefit/call: "For Indian builders" or "Now live"

**Tier 3 (Institutional grounding):**
- Brand: "aight" (very small, top or bottom)
- Tagline from website: "Where Indian businesses buy AI" (minimal, gray, bottom)
- URL: getaight.ai (footer, small)

**Tone:** Direct. No hype. No adjectives. Numbers speak for themselves.

---

### VISUAL_SYSTEM

**Color Palette:**
- **Background:** Off-white or very soft warm white (festive but not garish; aligns with enterprise aesthetic)
- **Typography:** Near-black for prices and primary text; mid-gray for tier 2/3 supporting text
- **Accent (optional):** One subtle color from Indian festive palette (deep saffron or deep green) used only in the separator line or logo lockup—reserved, not dominant

**Typography:**
- **Price numbers:** Large, geometric sans-serif (e.g., Inter, Grotesk, or similar—neutral, high-contrast)
  - ₹9: ~120–140px
  - ₹99: ~120–140px
- **Labels ("Image" / "Video"):** ~32–40px, same or lighter weight, positioned directly above/beside
- **Brand and footer text:** ~16–20px, medium or regular weight
- **Line height & spacing:** Generous vertical rhythm; prices separated by 60–100px of white space from brand/footer

**Layout Structure:**
- Vertical: top ¼ negative space → center ½ prices + labels → bottom ¼ brand + footer
- Symmetry or subtle asymmetry (e.g., prices left-aligned, labels right, creating a visual grid without clutter)
- No decorative graphics, icons, or photography
- Single vertical separator line (thin, 1–2px) between image and video pricing areas (optional; improves scannability)

---

### PRODUCTION_RECIPE

1. **Typeface Selection:** Download/license one neutral geometric sans-serif (must support Indian numerals; Unicode for ₹ symbol)
2. **Composition Grid:** 1080×1350px canvas. Divide into thirds vertically. Prices occupy center third.
3. **Color Mixing:** Define off-white background RGB/hex; near-black text RGB/hex; optional accent color (saffron #FF9F43 or forest green #2D5016, desaturated to ~60% saturation for restraint)
4. **Element Placement:**
   - "Image" label @ 480px from top, centered or left-aligned
   - ₹9 price @ 550px from top
   - "Video" label @ 750px from top
   - ₹99 price @ 820px from top
   - "aight" logo/wordmark @ 1150px from top (very small)
   - "Where Indian businesses buy AI" @ 1240px from top
   - "getaight.ai" @ 1300px from top
5. **Refinement:** Kern price numbers for visual balance. Test at 1080×1350 and at print sizes (300dpi for print).

---

### GENERATION_PROMPTS

**Single Executable Final Generation Prompt:**

> Create a minimalist premium promotional poster (4:5 ratio, vertical orientation) for an AI infrastructure company in India. The poster announces pricing for media-generation APIs:
> 
> **Visual hierarchy (top to bottom):**
> - Ample white space at the very top
> - The word "Image" in small, gray sans-serif at top-center
> - Below it, the price "₹9" in very large, bold geometric sans-serif (130pt equivalent), nearly black
> - A thin vertical separator line running between the left and right halves (optional; very subtle)
> - On the right side, the word "Video" in the same small gray sans-serif
> - Below it, "₹99" in the same large bold geometric sans-serif
> - Ample white space in the middle
> - Very bottom: the brand name "aight" in small sans-serif
> - Below that: "Where Indian businesses buy AI" in even smaller gray sans-serif
> - Footer: "getaight.ai" in tiny text
> 
> **Design principles:**
> - Background: soft off-white or warm cream (festive but not bright)
> - No icons, photos, or decorative elements
> - Typography carries 100% of the message
> - Pricing is the visual and conceptual centerpiece
> - Tone: institutional, direct, serious—not a discount retail flyer
> - Grid-based composition with generous negative space
> - Suitable for high-resolution print and digital display
> 
> Do not include promotional language like "Special Offer," "Now Available," or discount framing. Let the prices stand alone as the statement.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Brand logo/wordmark "aight":** Use official aight wordmark from getaight.ai (source: website). If unavailable in frozen snapshot, render as clean sans-serif lowercase "aight" in near-black.
- **Currency symbol (₹):** Render using Unicode U+20B9 or equivalent font glyph; ensure anti-aliasing is clean at large sizes.
- **Tagline text:** "Where Indian businesses buy AI" (exact phrasing from website homepage—mandatory for brand consistency).
- **URL:** "getaight.ai" (exact from website footer).

---

### AUDIO_AND_EDIT

**N/A.** Deliverable is a static poster; no audio, video edit, or animation.

---

### FAILURE_PREVENTION

1. **Price Prominence:** If image-generation price (₹9) is less visually dominant than video (₹99), rebalance by font size or position—both prices must be equally immediate and scannable.
2. **Brand Legibility at Thumbnail:** Shrink mockup to 300px width; verify "aight" and "getaight.ai" remain readable and positioned logically.
3. **Festive Context Check:** Ensure background color/tone evokes festive season without cacophony. Soft warm white + optional deep saffron/green accent is sufficient; avoid neon or overstimulating palettes.
4. **Enterprise Tone Preservation:** Remove any language or graphic flourishes that read as "discount" or "sale." Pricing is announcement, not promotion.
5. **Color Contrast:** Test near-black text on off-white background for WCAG AA compliance (contrast ratio ≥4.5:1). Test small footer text contrast separately.
6. **Print Readiness:** If poster will be printed, export at 300dpi; verify fonts embed or outline correctly; test on physical substrate (stock/finish appropriate for B2B office/event display).

---

### HARD_CONSTRAINT_CHECK

✓ Format: 4:5 vertical poster (executable as 1080×1350px or 2160×2700px print-ready)  
✓ Prices visible and immediately understandable (₹9 for image, ₹99 for video)  
✓ Premium/institutional tone, not retail flyer  
✓ Typography and hierarchy carry the design  
✓ Brand/product information sourced from getaight.ai only  
✓ Indian festive season context acknowledged (warm, clean aesthetic; no assumption of specific festival, but seasonal tone present)  
✓ Single concept, no alternatives  
✓ Production-ready prompts provided  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (primary): Brand positioning ("Where Indian businesses buy AI"), company entity name "aight," official tagline, target audience (Indian businesses), services (image and video generation), URL, founding principles (prepaid rupees, domestic GST, builder-focused, no-hype).

**Canon knowledge:** None consulted. Brand information and positioning constraints sourced entirely from getaight.ai website snapshot.

---

**END PRODUCTION PACKAGE**

## MESSAGE_AND_INFORMATION_HIERARCHY
**Tier 1 (Dominant – visual center):**
- The two prices: ₹9 and ₹99
- Matched line-height; neutral sans-serif; identical visual weight

**Tier 2 (Supporting structure):**
- What each price unlocks: "Image" / "Video" (small, above or beside prices)
- Single line of benefit/call: "For Indian builders" or "Now live"

**Tier 3 (Institutional grounding):**
- Brand: "aight" (very small, top or bottom)
- Tagline from website: "Where Indian businesses buy AI" (minimal, gray, bottom)
- URL: getaight.ai (footer, small)

**Tone:** Direct. No hype. No adjectives. Numbers speak for themselves.

---

### VISUAL_SYSTEM

**Color Palette:**
- **Background:** Off-white or very soft warm white (festive but not garish; aligns with enterprise aesthetic)
- **Typography:** Near-black for prices and primary text; mid-gray for tier 2/3 supporting text
- **Accent (optional):** One subtle color from Indian festive palette (deep saffron or deep green) used only in the separator line or logo lockup—reserved, not dominant

**Typography:**
- **Price numbers:** Large, geometric sans-serif (e.g., Inter, Grotesk, or similar—neutral, high-contrast)
  - ₹9: ~120–140px
  - ₹99: ~120–140px
- **Labels ("Image" / "Video"):** ~32–40px, same or lighter weight, positioned directly above/beside
- **Brand and footer text:** ~16–20px, medium or regular weight
- **Line height & spacing:** Generous vertical rhythm; prices separated by 60–100px of white space from brand/footer

**Layout Structure:**
- Vertical: top ¼ negative space → center ½ prices + labels → bottom ¼ brand + footer
- Symmetry or subtle asymmetry (e.g., prices left-aligned, labels right, creating a visual grid without clutter)
- No decorative graphics, icons, or photography
- Single vertical separator line (thin, 1–2px) between image and video pricing areas (optional; improves scannability)

---

### PRODUCTION_RECIPE

1. **Typeface Selection:** Download/license one neutral geometric sans-serif (must support Indian numerals; Unicode for ₹ symbol)
2. **Composition Grid:** 1080×1350px canvas. Divide into thirds vertically. Prices occupy center third.
3. **Color Mixing:** Define off-white background RGB/hex; near-black text RGB/hex; optional accent color (saffron #FF9F43 or forest green #2D5016, desaturated to ~60% saturation for restraint)
4. **Element Placement:**
   - "Image" label @ 480px from top, centered or left-aligned
   - ₹9 price @ 550px from top
   - "Video" label @ 750px from top
   - ₹99 price @ 820px from top
   - "aight" logo/wordmark @ 1150px from top (very small)
   - "Where Indian businesses buy AI" @ 1240px from top
   - "getaight.ai" @ 1300px from top
5. **Refinement:** Kern price numbers for visual balance. Test at 1080×1350 and at print sizes (300dpi for print).

---

### GENERATION_PROMPTS

**Single Executable Final Generation Prompt:**

> Create a minimalist premium promotional poster (4:5 ratio, vertical orientation) for an AI infrastructure company in India. The poster announces pricing for media-generation APIs:
> 
> **Visual hierarchy (top to bottom):**
> - Ample white space at the very top
> - The word "Image" in small, gray sans-serif at top-center
> - Below it, the price "₹9" in very large, bold geometric sans-serif (130pt equivalent), nearly black
> - A thin vertical separator line running between the left and right halves (optional; very subtle)
> - On the right side, the word "Video" in the same small gray sans-serif
> - Below it, "₹99" in the same large bold geometric sans-serif
> - Ample white space in the middle
> - Very bottom: the brand name "aight" in small sans-serif
> - Below that: "Where Indian businesses buy AI" in even smaller gray sans-serif
> - Footer: "getaight.ai" in tiny text
> 
> **Design principles:**
> - Background: soft off-white or warm cream (festive but not bright)
> - No icons, photos, or decorative elements
> - Typography carries 100% of the message
> - Pricing is the visual and conceptual centerpiece
> - Tone: institutional, direct, serious—not a discount retail flyer
> - Grid-based composition with generous negative space
> - Suitable for high-resolution print and digital display
> 
> Do not include promotional language like "Special Offer," "Now Available," or discount framing. Let the prices stand alone as the statement.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Brand logo/wordmark "aight":** Use official aight wordmark from getaight.ai (source: website). If unavailable in frozen snapshot, render as clean sans-serif lowercase "aight" in near-black.
- **Currency symbol (₹):** Render using Unicode U+20B9 or equivalent font glyph; ensure anti-aliasing is clean at large sizes.
- **Tagline text:** "Where Indian businesses buy AI" (exact phrasing from website homepage—mandatory for brand consistency).
- **URL:** "getaight.ai" (exact from website footer).

---

### AUDIO_AND_EDIT

**N/A.** Deliverable is a static poster; no audio, video edit, or animation.

---

### FAILURE_PREVENTION

1. **Price Prominence:** If image-generation price (₹9) is less visually dominant than video (₹99), rebalance by font size or position—both prices must be equally immediate and scannable.
2. **Brand Legibility at Thumbnail:** Shrink mockup to 300px width; verify "aight" and "getaight.ai" remain readable and positioned logically.
3. **Festive Context Check:** Ensure background color/tone evokes festive season without cacophony. Soft warm white + optional deep saffron/green accent is sufficient; avoid neon or overstimulating palettes.
4. **Enterprise Tone Preservation:** Remove any language or graphic flourishes that read as "discount" or "sale." Pricing is announcement, not promotion.
5. **Color Contrast:** Test near-black text on off-white background for WCAG AA compliance (contrast ratio ≥4.5:1). Test small footer text contrast separately.
6. **Print Readiness:** If poster will be printed, export at 300dpi; verify fonts embed or outline correctly; test on physical substrate (stock/finish appropriate for B2B office/event display).

---

### HARD_CONSTRAINT_CHECK

✓ Format: 4:5 vertical poster (executable as 1080×1350px or 2160×2700px print-ready)  
✓ Prices visible and immediately understandable (₹9 for image, ₹99 for video)  
✓ Premium/institutional tone, not retail flyer  
✓ Typography and hierarchy carry the design  
✓ Brand/product information sourced from getaight.ai only  
✓ Indian festive season context acknowledged (warm, clean aesthetic; no assumption of specific festival, but seasonal tone present)  
✓ Single concept, no alternatives  
✓ Production-ready prompts provided  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (primary): Brand positioning ("Where Indian businesses buy AI"), company entity name "aight," official tagline, target audience (Indian businesses), services (image and video generation), URL, founding principles (prepaid rupees, domestic GST, builder-focused, no-hype).

**Canon knowledge:** None consulted. Brand information and positioning constraints sourced entirely from getaight.ai website snapshot.

---

**END PRODUCTION PACKAGE**

## VISUAL_SYSTEM
**Color Palette:**
- **Background:** Off-white or very soft warm white (festive but not garish; aligns with enterprise aesthetic)
- **Typography:** Near-black for prices and primary text; mid-gray for tier 2/3 supporting text
- **Accent (optional):** One subtle color from Indian festive palette (deep saffron or deep green) used only in the separator line or logo lockup—reserved, not dominant

**Typography:**
- **Price numbers:** Large, geometric sans-serif (e.g., Inter, Grotesk, or similar—neutral, high-contrast)
  - ₹9: ~120–140px
  - ₹99: ~120–140px
- **Labels ("Image" / "Video"):** ~32–40px, same or lighter weight, positioned directly above/beside
- **Brand and footer text:** ~16–20px, medium or regular weight
- **Line height & spacing:** Generous vertical rhythm; prices separated by 60–100px of white space from brand/footer

**Layout Structure:**
- Vertical: top ¼ negative space → center ½ prices + labels → bottom ¼ brand + footer
- Symmetry or subtle asymmetry (e.g., prices left-aligned, labels right, creating a visual grid without clutter)
- No decorative graphics, icons, or photography
- Single vertical separator line (thin, 1–2px) between image and video pricing areas (optional; improves scannability)

---

### PRODUCTION_RECIPE

1. **Typeface Selection:** Download/license one neutral geometric sans-serif (must support Indian numerals; Unicode for ₹ symbol)
2. **Composition Grid:** 1080×1350px canvas. Divide into thirds vertically. Prices occupy center third.
3. **Color Mixing:** Define off-white background RGB/hex; near-black text RGB/hex; optional accent color (saffron #FF9F43 or forest green #2D5016, desaturated to ~60% saturation for restraint)
4. **Element Placement:**
   - "Image" label @ 480px from top, centered or left-aligned
   - ₹9 price @ 550px from top
   - "Video" label @ 750px from top
   - ₹99 price @ 820px from top
   - "aight" logo/wordmark @ 1150px from top (very small)
   - "Where Indian businesses buy AI" @ 1240px from top
   - "getaight.ai" @ 1300px from top
5. **Refinement:** Kern price numbers for visual balance. Test at 1080×1350 and at print sizes (300dpi for print).

---

### GENERATION_PROMPTS

**Single Executable Final Generation Prompt:**

> Create a minimalist premium promotional poster (4:5 ratio, vertical orientation) for an AI infrastructure company in India. The poster announces pricing for media-generation APIs:
> 
> **Visual hierarchy (top to bottom):**
> - Ample white space at the very top
> - The word "Image" in small, gray sans-serif at top-center
> - Below it, the price "₹9" in very large, bold geometric sans-serif (130pt equivalent), nearly black
> - A thin vertical separator line running between the left and right halves (optional; very subtle)
> - On the right side, the word "Video" in the same small gray sans-serif
> - Below it, "₹99" in the same large bold geometric sans-serif
> - Ample white space in the middle
> - Very bottom: the brand name "aight" in small sans-serif
> - Below that: "Where Indian businesses buy AI" in even smaller gray sans-serif
> - Footer: "getaight.ai" in tiny text
> 
> **Design principles:**
> - Background: soft off-white or warm cream (festive but not bright)
> - No icons, photos, or decorative elements
> - Typography carries 100% of the message
> - Pricing is the visual and conceptual centerpiece
> - Tone: institutional, direct, serious—not a discount retail flyer
> - Grid-based composition with generous negative space
> - Suitable for high-resolution print and digital display
> 
> Do not include promotional language like "Special Offer," "Now Available," or discount framing. Let the prices stand alone as the statement.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Brand logo/wordmark "aight":** Use official aight wordmark from getaight.ai (source: website). If unavailable in frozen snapshot, render as clean sans-serif lowercase "aight" in near-black.
- **Currency symbol (₹):** Render using Unicode U+20B9 or equivalent font glyph; ensure anti-aliasing is clean at large sizes.
- **Tagline text:** "Where Indian businesses buy AI" (exact phrasing from website homepage—mandatory for brand consistency).
- **URL:** "getaight.ai" (exact from website footer).

---

### AUDIO_AND_EDIT

**N/A.** Deliverable is a static poster; no audio, video edit, or animation.

---

### FAILURE_PREVENTION

1. **Price Prominence:** If image-generation price (₹9) is less visually dominant than video (₹99), rebalance by font size or position—both prices must be equally immediate and scannable.
2. **Brand Legibility at Thumbnail:** Shrink mockup to 300px width; verify "aight" and "getaight.ai" remain readable and positioned logically.
3. **Festive Context Check:** Ensure background color/tone evokes festive season without cacophony. Soft warm white + optional deep saffron/green accent is sufficient; avoid neon or overstimulating palettes.
4. **Enterprise Tone Preservation:** Remove any language or graphic flourishes that read as "discount" or "sale." Pricing is announcement, not promotion.
5. **Color Contrast:** Test near-black text on off-white background for WCAG AA compliance (contrast ratio ≥4.5:1). Test small footer text contrast separately.
6. **Print Readiness:** If poster will be printed, export at 300dpi; verify fonts embed or outline correctly; test on physical substrate (stock/finish appropriate for B2B office/event display).

---

### HARD_CONSTRAINT_CHECK

✓ Format: 4:5 vertical poster (executable as 1080×1350px or 2160×2700px print-ready)  
✓ Prices visible and immediately understandable (₹9 for image, ₹99 for video)  
✓ Premium/institutional tone, not retail flyer  
✓ Typography and hierarchy carry the design  
✓ Brand/product information sourced from getaight.ai only  
✓ Indian festive season context acknowledged (warm, clean aesthetic; no assumption of specific festival, but seasonal tone present)  
✓ Single concept, no alternatives  
✓ Production-ready prompts provided  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (primary): Brand positioning ("Where Indian businesses buy AI"), company entity name "aight," official tagline, target audience (Indian businesses), services (image and video generation), URL, founding principles (prepaid rupees, domestic GST, builder-focused, no-hype).

**Canon knowledge:** None consulted. Brand information and positioning constraints sourced entirely from getaight.ai website snapshot.

---

**END PRODUCTION PACKAGE**

## PRODUCTION_RECIPE
1. **Typeface Selection:** Download/license one neutral geometric sans-serif (must support Indian numerals; Unicode for ₹ symbol)
2. **Composition Grid:** 1080×1350px canvas. Divide into thirds vertically. Prices occupy center third.
3. **Color Mixing:** Define off-white background RGB/hex; near-black text RGB/hex; optional accent color (saffron #FF9F43 or forest green #2D5016, desaturated to ~60% saturation for restraint)
4. **Element Placement:**
   - "Image" label @ 480px from top, centered or left-aligned
   - ₹9 price @ 550px from top
   - "Video" label @ 750px from top
   - ₹99 price @ 820px from top
   - "aight" logo/wordmark @ 1150px from top (very small)
   - "Where Indian businesses buy AI" @ 1240px from top
   - "getaight.ai" @ 1300px from top
5. **Refinement:** Kern price numbers for visual balance. Test at 1080×1350 and at print sizes (300dpi for print).

---

### GENERATION_PROMPTS

**Single Executable Final Generation Prompt:**

> Create a minimalist premium promotional poster (4:5 ratio, vertical orientation) for an AI infrastructure company in India. The poster announces pricing for media-generation APIs:
> 
> **Visual hierarchy (top to bottom):**
> - Ample white space at the very top
> - The word "Image" in small, gray sans-serif at top-center
> - Below it, the price "₹9" in very large, bold geometric sans-serif (130pt equivalent), nearly black
> - A thin vertical separator line running between the left and right halves (optional; very subtle)
> - On the right side, the word "Video" in the same small gray sans-serif
> - Below it, "₹99" in the same large bold geometric sans-serif
> - Ample white space in the middle
> - Very bottom: the brand name "aight" in small sans-serif
> - Below that: "Where Indian businesses buy AI" in even smaller gray sans-serif
> - Footer: "getaight.ai" in tiny text
> 
> **Design principles:**
> - Background: soft off-white or warm cream (festive but not bright)
> - No icons, photos, or decorative elements
> - Typography carries 100% of the message
> - Pricing is the visual and conceptual centerpiece
> - Tone: institutional, direct, serious—not a discount retail flyer
> - Grid-based composition with generous negative space
> - Suitable for high-resolution print and digital display
> 
> Do not include promotional language like "Special Offer," "Now Available," or discount framing. Let the prices stand alone as the statement.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Brand logo/wordmark "aight":** Use official aight wordmark from getaight.ai (source: website). If unavailable in frozen snapshot, render as clean sans-serif lowercase "aight" in near-black.
- **Currency symbol (₹):** Render using Unicode U+20B9 or equivalent font glyph; ensure anti-aliasing is clean at large sizes.
- **Tagline text:** "Where Indian businesses buy AI" (exact phrasing from website homepage—mandatory for brand consistency).
- **URL:** "getaight.ai" (exact from website footer).

---

### AUDIO_AND_EDIT

**N/A.** Deliverable is a static poster; no audio, video edit, or animation.

---

### FAILURE_PREVENTION

1. **Price Prominence:** If image-generation price (₹9) is less visually dominant than video (₹99), rebalance by font size or position—both prices must be equally immediate and scannable.
2. **Brand Legibility at Thumbnail:** Shrink mockup to 300px width; verify "aight" and "getaight.ai" remain readable and positioned logically.
3. **Festive Context Check:** Ensure background color/tone evokes festive season without cacophony. Soft warm white + optional deep saffron/green accent is sufficient; avoid neon or overstimulating palettes.
4. **Enterprise Tone Preservation:** Remove any language or graphic flourishes that read as "discount" or "sale." Pricing is announcement, not promotion.
5. **Color Contrast:** Test near-black text on off-white background for WCAG AA compliance (contrast ratio ≥4.5:1). Test small footer text contrast separately.
6. **Print Readiness:** If poster will be printed, export at 300dpi; verify fonts embed or outline correctly; test on physical substrate (stock/finish appropriate for B2B office/event display).

---

### HARD_CONSTRAINT_CHECK

✓ Format: 4:5 vertical poster (executable as 1080×1350px or 2160×2700px print-ready)  
✓ Prices visible and immediately understandable (₹9 for image, ₹99 for video)  
✓ Premium/institutional tone, not retail flyer  
✓ Typography and hierarchy carry the design  
✓ Brand/product information sourced from getaight.ai only  
✓ Indian festive season context acknowledged (warm, clean aesthetic; no assumption of specific festival, but seasonal tone present)  
✓ Single concept, no alternatives  
✓ Production-ready prompts provided  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (primary): Brand positioning ("Where Indian businesses buy AI"), company entity name "aight," official tagline, target audience (Indian businesses), services (image and video generation), URL, founding principles (prepaid rupees, domestic GST, builder-focused, no-hype).

**Canon knowledge:** None consulted. Brand information and positioning constraints sourced entirely from getaight.ai website snapshot.

---

**END PRODUCTION PACKAGE**

## GENERATION_PROMPTS
**Single Executable Final Generation Prompt:**

> Create a minimalist premium promotional poster (4:5 ratio, vertical orientation) for an AI infrastructure company in India. The poster announces pricing for media-generation APIs:
> 
> **Visual hierarchy (top to bottom):**
> - Ample white space at the very top
> - The word "Image" in small, gray sans-serif at top-center
> - Below it, the price "₹9" in very large, bold geometric sans-serif (130pt equivalent), nearly black
> - A thin vertical separator line running between the left and right halves (optional; very subtle)
> - On the right side, the word "Video" in the same small gray sans-serif
> - Below it, "₹99" in the same large bold geometric sans-serif
> - Ample white space in the middle
> - Very bottom: the brand name "aight" in small sans-serif
> - Below that: "Where Indian businesses buy AI" in even smaller gray sans-serif
> - Footer: "getaight.ai" in tiny text
> 
> **Design principles:**
> - Background: soft off-white or warm cream (festive but not bright)
> - No icons, photos, or decorative elements
> - Typography carries 100% of the message
> - Pricing is the visual and conceptual centerpiece
> - Tone: institutional, direct, serious—not a discount retail flyer
> - Grid-based composition with generous negative space
> - Suitable for high-resolution print and digital display
> 
> Do not include promotional language like "Special Offer," "Now Available," or discount framing. Let the prices stand alone as the statement.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Brand logo/wordmark "aight":** Use official aight wordmark from getaight.ai (source: website). If unavailable in frozen snapshot, render as clean sans-serif lowercase "aight" in near-black.
- **Currency symbol (₹):** Render using Unicode U+20B9 or equivalent font glyph; ensure anti-aliasing is clean at large sizes.
- **Tagline text:** "Where Indian businesses buy AI" (exact phrasing from website homepage—mandatory for brand consistency).
- **URL:** "getaight.ai" (exact from website footer).

---

### AUDIO_AND_EDIT

**N/A.** Deliverable is a static poster; no audio, video edit, or animation.

---

### FAILURE_PREVENTION

1. **Price Prominence:** If image-generation price (₹9) is less visually dominant than video (₹99), rebalance by font size or position—both prices must be equally immediate and scannable.
2. **Brand Legibility at Thumbnail:** Shrink mockup to 300px width; verify "aight" and "getaight.ai" remain readable and positioned logically.
3. **Festive Context Check:** Ensure background color/tone evokes festive season without cacophony. Soft warm white + optional deep saffron/green accent is sufficient; avoid neon or overstimulating palettes.
4. **Enterprise Tone Preservation:** Remove any language or graphic flourishes that read as "discount" or "sale." Pricing is announcement, not promotion.
5. **Color Contrast:** Test near-black text on off-white background for WCAG AA compliance (contrast ratio ≥4.5:1). Test small footer text contrast separately.
6. **Print Readiness:** If poster will be printed, export at 300dpi; verify fonts embed or outline correctly; test on physical substrate (stock/finish appropriate for B2B office/event display).

---

### HARD_CONSTRAINT_CHECK

✓ Format: 4:5 vertical poster (executable as 1080×1350px or 2160×2700px print-ready)  
✓ Prices visible and immediately understandable (₹9 for image, ₹99 for video)  
✓ Premium/institutional tone, not retail flyer  
✓ Typography and hierarchy carry the design  
✓ Brand/product information sourced from getaight.ai only  
✓ Indian festive season context acknowledged (warm, clean aesthetic; no assumption of specific festival, but seasonal tone present)  
✓ Single concept, no alternatives  
✓ Production-ready prompts provided  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (primary): Brand positioning ("Where Indian businesses buy AI"), company entity name "aight," official tagline, target audience (Indian businesses), services (image and video generation), URL, founding principles (prepaid rupees, domestic GST, builder-focused, no-hype).

**Canon knowledge:** None consulted. Brand information and positioning constraints sourced entirely from getaight.ai website snapshot.

---

**END PRODUCTION PACKAGE**

## DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS
- **Brand logo/wordmark "aight":** Use official aight wordmark from getaight.ai (source: website). If unavailable in frozen snapshot, render as clean sans-serif lowercase "aight" in near-black.
- **Currency symbol (₹):** Render using Unicode U+20B9 or equivalent font glyph; ensure anti-aliasing is clean at large sizes.
- **Tagline text:** "Where Indian businesses buy AI" (exact phrasing from website homepage—mandatory for brand consistency).
- **URL:** "getaight.ai" (exact from website footer).

---

### AUDIO_AND_EDIT

**N/A.** Deliverable is a static poster; no audio, video edit, or animation.

---

### FAILURE_PREVENTION

1. **Price Prominence:** If image-generation price (₹9) is less visually dominant than video (₹99), rebalance by font size or position—both prices must be equally immediate and scannable.
2. **Brand Legibility at Thumbnail:** Shrink mockup to 300px width; verify "aight" and "getaight.ai" remain readable and positioned logically.
3. **Festive Context Check:** Ensure background color/tone evokes festive season without cacophony. Soft warm white + optional deep saffron/green accent is sufficient; avoid neon or overstimulating palettes.
4. **Enterprise Tone Preservation:** Remove any language or graphic flourishes that read as "discount" or "sale." Pricing is announcement, not promotion.
5. **Color Contrast:** Test near-black text on off-white background for WCAG AA compliance (contrast ratio ≥4.5:1). Test small footer text contrast separately.
6. **Print Readiness:** If poster will be printed, export at 300dpi; verify fonts embed or outline correctly; test on physical substrate (stock/finish appropriate for B2B office/event display).

---

### HARD_CONSTRAINT_CHECK

✓ Format: 4:5 vertical poster (executable as 1080×1350px or 2160×2700px print-ready)  
✓ Prices visible and immediately understandable (₹9 for image, ₹99 for video)  
✓ Premium/institutional tone, not retail flyer  
✓ Typography and hierarchy carry the design  
✓ Brand/product information sourced from getaight.ai only  
✓ Indian festive season context acknowledged (warm, clean aesthetic; no assumption of specific festival, but seasonal tone present)  
✓ Single concept, no alternatives  
✓ Production-ready prompts provided  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (primary): Brand positioning ("Where Indian businesses buy AI"), company entity name "aight," official tagline, target audience (Indian businesses), services (image and video generation), URL, founding principles (prepaid rupees, domestic GST, builder-focused, no-hype).

**Canon knowledge:** None consulted. Brand information and positioning constraints sourced entirely from getaight.ai website snapshot.

---

**END PRODUCTION PACKAGE**

## FAILURE_PREVENTION
1. **Price Prominence:** If image-generation price (₹9) is less visually dominant than video (₹99), rebalance by font size or position—both prices must be equally immediate and scannable.
2. **Brand Legibility at Thumbnail:** Shrink mockup to 300px width; verify "aight" and "getaight.ai" remain readable and positioned logically.
3. **Festive Context Check:** Ensure background color/tone evokes festive season without cacophony. Soft warm white + optional deep saffron/green accent is sufficient; avoid neon or overstimulating palettes.
4. **Enterprise Tone Preservation:** Remove any language or graphic flourishes that read as "discount" or "sale." Pricing is announcement, not promotion.
5. **Color Contrast:** Test near-black text on off-white background for WCAG AA compliance (contrast ratio ≥4.5:1). Test small footer text contrast separately.
6. **Print Readiness:** If poster will be printed, export at 300dpi; verify fonts embed or outline correctly; test on physical substrate (stock/finish appropriate for B2B office/event display).

---

### HARD_CONSTRAINT_CHECK

✓ Format: 4:5 vertical poster (executable as 1080×1350px or 2160×2700px print-ready)  
✓ Prices visible and immediately understandable (₹9 for image, ₹99 for video)  
✓ Premium/institutional tone, not retail flyer  
✓ Typography and hierarchy carry the design  
✓ Brand/product information sourced from getaight.ai only  
✓ Indian festive season context acknowledged (warm, clean aesthetic; no assumption of specific festival, but seasonal tone present)  
✓ Single concept, no alternatives  
✓ Production-ready prompts provided  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (primary): Brand positioning ("Where Indian businesses buy AI"), company entity name "aight," official tagline, target audience (Indian businesses), services (image and video generation), URL, founding principles (prepaid rupees, domestic GST, builder-focused, no-hype).

**Canon knowledge:** None consulted. Brand information and positioning constraints sourced entirely from getaight.ai website snapshot.

---

**END PRODUCTION PACKAGE**

## HARD_CONSTRAINT_CHECK
✓ Format: 4:5 vertical poster (executable as 1080×1350px or 2160×2700px print-ready)  
✓ Prices visible and immediately understandable (₹9 for image, ₹99 for video)  
✓ Premium/institutional tone, not retail flyer  
✓ Typography and hierarchy carry the design  
✓ Brand/product information sourced from getaight.ai only  
✓ Indian festive season context acknowledged (warm, clean aesthetic; no assumption of specific festival, but seasonal tone present)  
✓ Single concept, no alternatives  
✓ Production-ready prompts provided  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources used:**
- **https://getaight.ai** (primary): Brand positioning ("Where Indian businesses buy AI"), company entity name "aight," official tagline, target audience (Indian businesses), services (image and video generation), URL, founding principles (prepaid rupees, domestic GST, builder-focused, no-hype).

**Canon knowledge:** None consulted. Brand information and positioning constraints sourced entirely from getaight.ai website snapshot.

---

**END PRODUCTION PACKAGE**

## GENERATE I10
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I11 — B02

Source key: E037-haiku-full-canon-B02-R2
Use frozen brief B02 from the top of this file.

## DELIVERABLE
A single 4:5 (portrait) premium promotional poster for aight's media-generation API, targetted at Indian businesses during festive season. Format optimized for social, mobile, and print collateral.

---

### OBJECTIVE_INTERPRETATION
Convert aight's core commercial proposition (image ₹9, video ₹99) into a credible, premium positioning that:
- Makes both prices immediately scannable and compelling
- Aligns with brand identity: serious AI infrastructure, domestic, founder-led, control-focused
- Appeals to Indian businesses' need for cost visibility and ROI clarity
- Signals infrastructure quality, not discount retail
- Works in festive season context (value, abundance, abundance-for-the-right-price)

---

### CORE_CREATIVE_IDEA
**Typographic hierarchy as merchant's counter:** The poster mirrors aight's own design language—a clean merchant counter where every element earns its placement. The two prices sit as inventory items on a shelf, with supporting structure that emphasizes:
1. Transparency (what you see is what you pay)
2. Domestic preparation (rupees, simplicity, no hidden layers)
3. Infrastructure quality (precise, controlled, professional)

Avoid graphic flourish; let the numbers and their context do the persuasion. The festive season becomes a framing device for "abundance at control"—not discount, but abundance that fits within discipline.

---

### MESSAGE_AND_INFORMATION_HIERARCHY

**Primary (Top ~25% of poster):**
Wordmark + festive seasonal marker
"Image + Video. Aight Rates."  
(or) "Generate. India-Ready."

**Secondary (Center block ~50%—THE SHELF):**
```
₹9      ₹99
Image   Video
```
With sub-lines:
- "Per image generation"
- "Per video generation"
- Or simply visual markers (icon or label)

**Supporting (Bottom ~25%):**
- Tagline reinforcing brand essence: "Control, Rupees, No Surprises" or "Prepaid. Domestic. Yours."
- Subtle reference to the merchant/counter metaphor: "Where Indian builders buy media AI"
- Minimal call-to-action: "getaight.ai" + WhatsApp handle or "Talk to us"

**Tone:** Confident, spare, legible at mobile scale.

---

### VISUAL_SYSTEM

**Typography (Execution-Level Guidance):**
- **Headings:** Geometric sans-serif, high contrast, bold weight (Aight's aesthetic reads modern-infrastructure, not playful). Recommend: Inter Black, IBM Plex Sans Bold, or equivalent clean sans.
- **Prices:** XL, dominant, set in a distinct weight or color to ensure immediate focus.
- **Supporting text:** Light/regular weight, same typeface family, generous line spacing for clarity.

**Color Palette:**
- **Primary:** Deep, professional background (charcoal, navy, or near-black) to establish premium infrastructure feel.
- **Accent:** Single accent color for prices—either warm gold/orange (festive, prosperity, auspicious in Indian context) or crisp white/cream for maximum contrast. Avoid bright neons; maintain institutional credibility.
- **Alternative:** Minimal color—prices in a single bold color (gold or white), rest monochromatic.

**Layout:**
- Full-bleed background, minimal margins.
- Vertical rhythm: top section (10%), price shelf (50%), bottom section (40%).
- Prices centered, substantial whitespace around them (breathe the hierarchy).
- Clean baseline grid; every line intentional.

**Visual Assets:**
- No illustrations or decorative icons beyond minimal geometric markers (e.g., a thin line separating sections, a small merchant-counter reference).
- Festive element (if needed): A subtle pattern or texture in the background, or a single embellishment in the bottom corner—but keep it refined, not garish.
- Aight wordmark placed clearly (likely top-left or top-center).

---

### PRODUCTION_RECIPE

**Input Specification:**
- Canvas: 1080×1350 px (4:5 aspect ratio, standard for Instagram Stories/Reels, mobile ads, printable at 300 DPI as 14.4" × 18")
- 300 DPI output for print; 72 DPI for web.

**Build Process:**
1. **Base layer:** Solid background color (charcoal or navy, RGB: 20, 24, 35 or similar deep tone).
2. **Typography layer:** 
   - Aight wordmark (top, 12% from top).
   - Festive/seasonal marker (small text or emoji, e.g., "This Festive Season" or similar, 8pt).
   - Main headline (e.g., "Generate. Get Rates." centered, 48–60pt bold).
3. **Price shelf (center):**
   - Two columns: left "₹9 Image", right "₹99 Video".
   - Price numerals: 120–150pt, bold, accent color (gold #D4AF37 or white #FFFFFF on dark ground).
   - Sub-labels: 14–18pt, light gray or white, supporting text.
4. **Bottom section:**
   - Tagline: 16–20pt, light weight.
   - Contact line: "getaight.ai" or "WhatsApp: [link]", minimal size.
5. **Refinement:** Adjust kerning, leading, and whitespace for premium feel; ensure legibility at 300px width (mobile preview).

**Design Notes:**
- Avoid centered-text softness; use ranged left/right alignment or strong centering for hierarchy.
- Leave generous whitespace; cramped = discount retail.
- No drop shadows, gradients, or effects unless absolutely necessary.

---

### GENERATION_PROMPTS

**Final Executable Prompt for Image Generation:**

> Create a premium 4:5 portrait promotional poster for an AI infrastructure company. 
> 
> Background: Solid deep charcoal (almost black), professional and institutional. No gradients or texture.
>
> Top section (10% of height): Place the wordmark "aight" in crisp white, sans-serif, modern style. Below it, small text in light gray: "This Festive Season".
>
> Center section (50% of height): Large, dominant headline text in clean white sans-serif: "Generate at Aight Rates." Beneath this, two large pricing blocks side by side, separated by whitespace:
> - Left: The symbol "₹9" in very large, bold typeface (120pt equivalent, dark gold or bright white), with supporting text "Per Image" underneath in small light gray text.
> - Right: The symbol "₹99" in the same large, bold typeface, with supporting text "Per Video" underneath in matching gray.
>
> Bottom section (40% of height): 
> - Centered, modest tagline in light gray: "Prepaid in Rupees. Domestic GST. Control Your Spend."
> - Below that, a line in white: "getaight.ai"
> - Very small text: "Where Indian businesses buy media AI"
>
> Overall aesthetic: Institutional, transparent, serious infrastructure feel. Maximum legibility on mobile (minimum 300px wide). Use only clean sans-serif typography (no serifs, no scripts). No illustrations, icons, or decorative elements. Minimal whitespace around prices to emphasize hierarchy. Print-ready, professional, premium positioning.

**Alternative Tighter Prompt (if strict generation control needed):**

> Premium dark poster, 4:5 format. Background: charcoal black. Top: "aight" wordmark (white, sans-serif). Center: Two large prices, ₹9 and ₹99, bold white text on black, with labels "Image" and "Video" in gray below. Bottom: "getaight.ai" and tagline "Domestic. Transparent. For Builders." Typography-led design, no illustrations. Festive season framing implicit in abundance messaging. Institutional tone.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Deterministic (Fixed, Non-Generated):**
- Exact pricing figures: ₹9 and ₹99 (must not be altered by generation)
- Aight wordmark/logo (use official brand asset; do not regenerate)
- Website URL: getaight.ai (exact spelling, no variation)
- Contact method reference: WhatsApp or direct domain (use official)
- Color hex codes for accent (if gold used: #D4AF37; if white: #FFFFFF; background: #141823 or similar approved dark tone)

**Non-Generative (Post-Production Assembly):**
- Overlay aight's official wordmark on generated background if generation does not include it with sufficient fidelity.
- If generated prices are unreadable or misaligned, replace with vector text at exact sizes and positions.
- Manual spell-check and proofing of all supporting text.
- Export at 1080×1350 px (4:5), then verify legibility at 300px width (mobile preview).

---

### AUDIO_AND_EDIT

**Not applicable for a static poster.** 

If this poster is repurposed for a video (e.g., 15-second Instagram Reel with animated price reveal), consider:
- Subtle ambient sound or a single clean tone (no music; aligns with institutional brand).
- Price numbers animate in sequentially or expand into frame, with a voiceover: "Image generation at ₹9. Video generation at ₹99. Aight."
- Duration: 3 seconds for price reveal, with 2-second hold and 2-second call-to-action (contact/website URL).

---

### FAILURE_PREVENTION

**High-Risk Failure Modes:**

1. **Prices illegible on mobile:** Mitigation—ensure ₹9 and ₹99 are minimum 60pt equivalent at 300px width; test preview at that scale.

2. **Discount-retail visual tone:** Mitigation—avoid bright gradients, shadow effects, or ornamental graphics. Hold to monochromatic + single accent color. Trust typography entirely.

3. **Festive season feels cheap:** Mitigation—do not use cartoon or bright colors. Use gold only as a sophisticated accent (high-contrast, minimal use), not as pervasive fill. Retain institutional neutrality.

4. **Hierarchy unclear:** Mitigation—ensure prices occupy 40–50% of poster's height; all other text is subordinate in size and weight. No competing focal points.

5. **Contact information weak:** Mitigation—include "getaight.ai" or WhatsApp in readable size (min 12pt), positioned clearly at bottom. If WhatsApp, include a small icon or prefix label.

6. **Wordmark placement wrong:** Mitigation—verify aight's official logo specification and placement before generation; use deterministic overlay if generation misplaces it.

7. **Text cut off on rounded corners (mobile):** Mitigation—avoid placing critical text in top/bottom corners; provide 50px safe margin on all edges for mobile viewing.

**Testing Checklist:**
- [ ] Legible at 300px width (mobile preview scale).
- [ ] Prices immediately scannable (eyes land on ₹9 and ₹99 within 2 seconds).
- [ ] No color or tone reads as "discount retailer" (compare to institutional finance/SaaS imagery).
- [ ] Aight wordmark present and correctly positioned.
- [ ] All contact information accurate (getaight.ai, WhatsApp handle).
- [ ] Suitable for print at 300 DPI and web at 72 DPI (no quality loss).

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 poster confirmed.  
✅ **Commercial proposition:** ₹9 (image) and ₹99 (video) clearly displayed, immediately understandable.  
✅ **Tone:** Serious AI infrastructure/product company, not discount retail—achieved via spare typography and institutional color/layout choices.  
✅ **Design focus:** Typography and information hierarchy are primary tools; minimal supplementary graphics.  
✅ **Source:** All brand and product information sourced exclusively from https://getaight.ai.  
✅ **Single deliverable:** One poster, one concept—no alternatives.  
✅ **Festive season relevance:** Positioned as "abundance at control," aligns with Indian festive value proposition without garish visual cues.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources Used:**
- **https://getaight.ai** (website snapshot): Brand positioning, messaging tone, product offering (image and video generation), target audience (Indian businesses), brand values (transparency, domestic, founder-led support, cost control, no hidden fees).

**Canon Knowledge Library:** Not consulted. Brand and product information obtained solely from aight's official website per customer instruction.

**Key Brand Insights Applied:**
- Aight's self-positioning as "Where Indian businesses buy AI" informs tagline direction.
- Emphasis on "prepaid rupees," "domestic GST invoice," and "hard caps" translates to supporting copy: "Prepaid. Domestic. Transparent."
- Founder-led support philosophy (WhatsApp contact, no ticket queue) supports direct contact CTA.
- Merchant/counter metaphor in website copy informed visual shelf structure for prices.
- No glossy AI jargon; clean, legible infrastructure aesthetic.

---

**END OF PRODUCTION PACKAGE**

## OBJECTIVE_INTERPRETATION
Convert aight's core commercial proposition (image ₹9, video ₹99) into a credible, premium positioning that:
- Makes both prices immediately scannable and compelling
- Aligns with brand identity: serious AI infrastructure, domestic, founder-led, control-focused
- Appeals to Indian businesses' need for cost visibility and ROI clarity
- Signals infrastructure quality, not discount retail
- Works in festive season context (value, abundance, abundance-for-the-right-price)

---

### CORE_CREATIVE_IDEA
**Typographic hierarchy as merchant's counter:** The poster mirrors aight's own design language—a clean merchant counter where every element earns its placement. The two prices sit as inventory items on a shelf, with supporting structure that emphasizes:
1. Transparency (what you see is what you pay)
2. Domestic preparation (rupees, simplicity, no hidden layers)
3. Infrastructure quality (precise, controlled, professional)

Avoid graphic flourish; let the numbers and their context do the persuasion. The festive season becomes a framing device for "abundance at control"—not discount, but abundance that fits within discipline.

---

### MESSAGE_AND_INFORMATION_HIERARCHY

**Primary (Top ~25% of poster):**
Wordmark + festive seasonal marker
"Image + Video. Aight Rates."  
(or) "Generate. India-Ready."

**Secondary (Center block ~50%—THE SHELF):**
```
₹9      ₹99
Image   Video
```
With sub-lines:
- "Per image generation"
- "Per video generation"
- Or simply visual markers (icon or label)

**Supporting (Bottom ~25%):**
- Tagline reinforcing brand essence: "Control, Rupees, No Surprises" or "Prepaid. Domestic. Yours."
- Subtle reference to the merchant/counter metaphor: "Where Indian builders buy media AI"
- Minimal call-to-action: "getaight.ai" + WhatsApp handle or "Talk to us"

**Tone:** Confident, spare, legible at mobile scale.

---

### VISUAL_SYSTEM

**Typography (Execution-Level Guidance):**
- **Headings:** Geometric sans-serif, high contrast, bold weight (Aight's aesthetic reads modern-infrastructure, not playful). Recommend: Inter Black, IBM Plex Sans Bold, or equivalent clean sans.
- **Prices:** XL, dominant, set in a distinct weight or color to ensure immediate focus.
- **Supporting text:** Light/regular weight, same typeface family, generous line spacing for clarity.

**Color Palette:**
- **Primary:** Deep, professional background (charcoal, navy, or near-black) to establish premium infrastructure feel.
- **Accent:** Single accent color for prices—either warm gold/orange (festive, prosperity, auspicious in Indian context) or crisp white/cream for maximum contrast. Avoid bright neons; maintain institutional credibility.
- **Alternative:** Minimal color—prices in a single bold color (gold or white), rest monochromatic.

**Layout:**
- Full-bleed background, minimal margins.
- Vertical rhythm: top section (10%), price shelf (50%), bottom section (40%).
- Prices centered, substantial whitespace around them (breathe the hierarchy).
- Clean baseline grid; every line intentional.

**Visual Assets:**
- No illustrations or decorative icons beyond minimal geometric markers (e.g., a thin line separating sections, a small merchant-counter reference).
- Festive element (if needed): A subtle pattern or texture in the background, or a single embellishment in the bottom corner—but keep it refined, not garish.
- Aight wordmark placed clearly (likely top-left or top-center).

---

### PRODUCTION_RECIPE

**Input Specification:**
- Canvas: 1080×1350 px (4:5 aspect ratio, standard for Instagram Stories/Reels, mobile ads, printable at 300 DPI as 14.4" × 18")
- 300 DPI output for print; 72 DPI for web.

**Build Process:**
1. **Base layer:** Solid background color (charcoal or navy, RGB: 20, 24, 35 or similar deep tone).
2. **Typography layer:** 
   - Aight wordmark (top, 12% from top).
   - Festive/seasonal marker (small text or emoji, e.g., "This Festive Season" or similar, 8pt).
   - Main headline (e.g., "Generate. Get Rates." centered, 48–60pt bold).
3. **Price shelf (center):**
   - Two columns: left "₹9 Image", right "₹99 Video".
   - Price numerals: 120–150pt, bold, accent color (gold #D4AF37 or white #FFFFFF on dark ground).
   - Sub-labels: 14–18pt, light gray or white, supporting text.
4. **Bottom section:**
   - Tagline: 16–20pt, light weight.
   - Contact line: "getaight.ai" or "WhatsApp: [link]", minimal size.
5. **Refinement:** Adjust kerning, leading, and whitespace for premium feel; ensure legibility at 300px width (mobile preview).

**Design Notes:**
- Avoid centered-text softness; use ranged left/right alignment or strong centering for hierarchy.
- Leave generous whitespace; cramped = discount retail.
- No drop shadows, gradients, or effects unless absolutely necessary.

---

### GENERATION_PROMPTS

**Final Executable Prompt for Image Generation:**

> Create a premium 4:5 portrait promotional poster for an AI infrastructure company. 
> 
> Background: Solid deep charcoal (almost black), professional and institutional. No gradients or texture.
>
> Top section (10% of height): Place the wordmark "aight" in crisp white, sans-serif, modern style. Below it, small text in light gray: "This Festive Season".
>
> Center section (50% of height): Large, dominant headline text in clean white sans-serif: "Generate at Aight Rates." Beneath this, two large pricing blocks side by side, separated by whitespace:
> - Left: The symbol "₹9" in very large, bold typeface (120pt equivalent, dark gold or bright white), with supporting text "Per Image" underneath in small light gray text.
> - Right: The symbol "₹99" in the same large, bold typeface, with supporting text "Per Video" underneath in matching gray.
>
> Bottom section (40% of height): 
> - Centered, modest tagline in light gray: "Prepaid in Rupees. Domestic GST. Control Your Spend."
> - Below that, a line in white: "getaight.ai"
> - Very small text: "Where Indian businesses buy media AI"
>
> Overall aesthetic: Institutional, transparent, serious infrastructure feel. Maximum legibility on mobile (minimum 300px wide). Use only clean sans-serif typography (no serifs, no scripts). No illustrations, icons, or decorative elements. Minimal whitespace around prices to emphasize hierarchy. Print-ready, professional, premium positioning.

**Alternative Tighter Prompt (if strict generation control needed):**

> Premium dark poster, 4:5 format. Background: charcoal black. Top: "aight" wordmark (white, sans-serif). Center: Two large prices, ₹9 and ₹99, bold white text on black, with labels "Image" and "Video" in gray below. Bottom: "getaight.ai" and tagline "Domestic. Transparent. For Builders." Typography-led design, no illustrations. Festive season framing implicit in abundance messaging. Institutional tone.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Deterministic (Fixed, Non-Generated):**
- Exact pricing figures: ₹9 and ₹99 (must not be altered by generation)
- Aight wordmark/logo (use official brand asset; do not regenerate)
- Website URL: getaight.ai (exact spelling, no variation)
- Contact method reference: WhatsApp or direct domain (use official)
- Color hex codes for accent (if gold used: #D4AF37; if white: #FFFFFF; background: #141823 or similar approved dark tone)

**Non-Generative (Post-Production Assembly):**
- Overlay aight's official wordmark on generated background if generation does not include it with sufficient fidelity.
- If generated prices are unreadable or misaligned, replace with vector text at exact sizes and positions.
- Manual spell-check and proofing of all supporting text.
- Export at 1080×1350 px (4:5), then verify legibility at 300px width (mobile preview).

---

### AUDIO_AND_EDIT

**Not applicable for a static poster.** 

If this poster is repurposed for a video (e.g., 15-second Instagram Reel with animated price reveal), consider:
- Subtle ambient sound or a single clean tone (no music; aligns with institutional brand).
- Price numbers animate in sequentially or expand into frame, with a voiceover: "Image generation at ₹9. Video generation at ₹99. Aight."
- Duration: 3 seconds for price reveal, with 2-second hold and 2-second call-to-action (contact/website URL).

---

### FAILURE_PREVENTION

**High-Risk Failure Modes:**

1. **Prices illegible on mobile:** Mitigation—ensure ₹9 and ₹99 are minimum 60pt equivalent at 300px width; test preview at that scale.

2. **Discount-retail visual tone:** Mitigation—avoid bright gradients, shadow effects, or ornamental graphics. Hold to monochromatic + single accent color. Trust typography entirely.

3. **Festive season feels cheap:** Mitigation—do not use cartoon or bright colors. Use gold only as a sophisticated accent (high-contrast, minimal use), not as pervasive fill. Retain institutional neutrality.

4. **Hierarchy unclear:** Mitigation—ensure prices occupy 40–50% of poster's height; all other text is subordinate in size and weight. No competing focal points.

5. **Contact information weak:** Mitigation—include "getaight.ai" or WhatsApp in readable size (min 12pt), positioned clearly at bottom. If WhatsApp, include a small icon or prefix label.

6. **Wordmark placement wrong:** Mitigation—verify aight's official logo specification and placement before generation; use deterministic overlay if generation misplaces it.

7. **Text cut off on rounded corners (mobile):** Mitigation—avoid placing critical text in top/bottom corners; provide 50px safe margin on all edges for mobile viewing.

**Testing Checklist:**
- [ ] Legible at 300px width (mobile preview scale).
- [ ] Prices immediately scannable (eyes land on ₹9 and ₹99 within 2 seconds).
- [ ] No color or tone reads as "discount retailer" (compare to institutional finance/SaaS imagery).
- [ ] Aight wordmark present and correctly positioned.
- [ ] All contact information accurate (getaight.ai, WhatsApp handle).
- [ ] Suitable for print at 300 DPI and web at 72 DPI (no quality loss).

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 poster confirmed.  
✅ **Commercial proposition:** ₹9 (image) and ₹99 (video) clearly displayed, immediately understandable.  
✅ **Tone:** Serious AI infrastructure/product company, not discount retail—achieved via spare typography and institutional color/layout choices.  
✅ **Design focus:** Typography and information hierarchy are primary tools; minimal supplementary graphics.  
✅ **Source:** All brand and product information sourced exclusively from https://getaight.ai.  
✅ **Single deliverable:** One poster, one concept—no alternatives.  
✅ **Festive season relevance:** Positioned as "abundance at control," aligns with Indian festive value proposition without garish visual cues.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources Used:**
- **https://getaight.ai** (website snapshot): Brand positioning, messaging tone, product offering (image and video generation), target audience (Indian businesses), brand values (transparency, domestic, founder-led support, cost control, no hidden fees).

**Canon Knowledge Library:** Not consulted. Brand and product information obtained solely from aight's official website per customer instruction.

**Key Brand Insights Applied:**
- Aight's self-positioning as "Where Indian businesses buy AI" informs tagline direction.
- Emphasis on "prepaid rupees," "domestic GST invoice," and "hard caps" translates to supporting copy: "Prepaid. Domestic. Transparent."
- Founder-led support philosophy (WhatsApp contact, no ticket queue) supports direct contact CTA.
- Merchant/counter metaphor in website copy informed visual shelf structure for prices.
- No glossy AI jargon; clean, legible infrastructure aesthetic.

---

**END OF PRODUCTION PACKAGE**

## CORE_CREATIVE_IDEA
**Typographic hierarchy as merchant's counter:** The poster mirrors aight's own design language—a clean merchant counter where every element earns its placement. The two prices sit as inventory items on a shelf, with supporting structure that emphasizes:
1. Transparency (what you see is what you pay)
2. Domestic preparation (rupees, simplicity, no hidden layers)
3. Infrastructure quality (precise, controlled, professional)

Avoid graphic flourish; let the numbers and their context do the persuasion. The festive season becomes a framing device for "abundance at control"—not discount, but abundance that fits within discipline.

---

### MESSAGE_AND_INFORMATION_HIERARCHY

**Primary (Top ~25% of poster):**
Wordmark + festive seasonal marker
"Image + Video. Aight Rates."  
(or) "Generate. India-Ready."

**Secondary (Center block ~50%—THE SHELF):**
```
₹9      ₹99
Image   Video
```
With sub-lines:
- "Per image generation"
- "Per video generation"
- Or simply visual markers (icon or label)

**Supporting (Bottom ~25%):**
- Tagline reinforcing brand essence: "Control, Rupees, No Surprises" or "Prepaid. Domestic. Yours."
- Subtle reference to the merchant/counter metaphor: "Where Indian builders buy media AI"
- Minimal call-to-action: "getaight.ai" + WhatsApp handle or "Talk to us"

**Tone:** Confident, spare, legible at mobile scale.

---

### VISUAL_SYSTEM

**Typography (Execution-Level Guidance):**
- **Headings:** Geometric sans-serif, high contrast, bold weight (Aight's aesthetic reads modern-infrastructure, not playful). Recommend: Inter Black, IBM Plex Sans Bold, or equivalent clean sans.
- **Prices:** XL, dominant, set in a distinct weight or color to ensure immediate focus.
- **Supporting text:** Light/regular weight, same typeface family, generous line spacing for clarity.

**Color Palette:**
- **Primary:** Deep, professional background (charcoal, navy, or near-black) to establish premium infrastructure feel.
- **Accent:** Single accent color for prices—either warm gold/orange (festive, prosperity, auspicious in Indian context) or crisp white/cream for maximum contrast. Avoid bright neons; maintain institutional credibility.
- **Alternative:** Minimal color—prices in a single bold color (gold or white), rest monochromatic.

**Layout:**
- Full-bleed background, minimal margins.
- Vertical rhythm: top section (10%), price shelf (50%), bottom section (40%).
- Prices centered, substantial whitespace around them (breathe the hierarchy).
- Clean baseline grid; every line intentional.

**Visual Assets:**
- No illustrations or decorative icons beyond minimal geometric markers (e.g., a thin line separating sections, a small merchant-counter reference).
- Festive element (if needed): A subtle pattern or texture in the background, or a single embellishment in the bottom corner—but keep it refined, not garish.
- Aight wordmark placed clearly (likely top-left or top-center).

---

### PRODUCTION_RECIPE

**Input Specification:**
- Canvas: 1080×1350 px (4:5 aspect ratio, standard for Instagram Stories/Reels, mobile ads, printable at 300 DPI as 14.4" × 18")
- 300 DPI output for print; 72 DPI for web.

**Build Process:**
1. **Base layer:** Solid background color (charcoal or navy, RGB: 20, 24, 35 or similar deep tone).
2. **Typography layer:** 
   - Aight wordmark (top, 12% from top).
   - Festive/seasonal marker (small text or emoji, e.g., "This Festive Season" or similar, 8pt).
   - Main headline (e.g., "Generate. Get Rates." centered, 48–60pt bold).
3. **Price shelf (center):**
   - Two columns: left "₹9 Image", right "₹99 Video".
   - Price numerals: 120–150pt, bold, accent color (gold #D4AF37 or white #FFFFFF on dark ground).
   - Sub-labels: 14–18pt, light gray or white, supporting text.
4. **Bottom section:**
   - Tagline: 16–20pt, light weight.
   - Contact line: "getaight.ai" or "WhatsApp: [link]", minimal size.
5. **Refinement:** Adjust kerning, leading, and whitespace for premium feel; ensure legibility at 300px width (mobile preview).

**Design Notes:**
- Avoid centered-text softness; use ranged left/right alignment or strong centering for hierarchy.
- Leave generous whitespace; cramped = discount retail.
- No drop shadows, gradients, or effects unless absolutely necessary.

---

### GENERATION_PROMPTS

**Final Executable Prompt for Image Generation:**

> Create a premium 4:5 portrait promotional poster for an AI infrastructure company. 
> 
> Background: Solid deep charcoal (almost black), professional and institutional. No gradients or texture.
>
> Top section (10% of height): Place the wordmark "aight" in crisp white, sans-serif, modern style. Below it, small text in light gray: "This Festive Season".
>
> Center section (50% of height): Large, dominant headline text in clean white sans-serif: "Generate at Aight Rates." Beneath this, two large pricing blocks side by side, separated by whitespace:
> - Left: The symbol "₹9" in very large, bold typeface (120pt equivalent, dark gold or bright white), with supporting text "Per Image" underneath in small light gray text.
> - Right: The symbol "₹99" in the same large, bold typeface, with supporting text "Per Video" underneath in matching gray.
>
> Bottom section (40% of height): 
> - Centered, modest tagline in light gray: "Prepaid in Rupees. Domestic GST. Control Your Spend."
> - Below that, a line in white: "getaight.ai"
> - Very small text: "Where Indian businesses buy media AI"
>
> Overall aesthetic: Institutional, transparent, serious infrastructure feel. Maximum legibility on mobile (minimum 300px wide). Use only clean sans-serif typography (no serifs, no scripts). No illustrations, icons, or decorative elements. Minimal whitespace around prices to emphasize hierarchy. Print-ready, professional, premium positioning.

**Alternative Tighter Prompt (if strict generation control needed):**

> Premium dark poster, 4:5 format. Background: charcoal black. Top: "aight" wordmark (white, sans-serif). Center: Two large prices, ₹9 and ₹99, bold white text on black, with labels "Image" and "Video" in gray below. Bottom: "getaight.ai" and tagline "Domestic. Transparent. For Builders." Typography-led design, no illustrations. Festive season framing implicit in abundance messaging. Institutional tone.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Deterministic (Fixed, Non-Generated):**
- Exact pricing figures: ₹9 and ₹99 (must not be altered by generation)
- Aight wordmark/logo (use official brand asset; do not regenerate)
- Website URL: getaight.ai (exact spelling, no variation)
- Contact method reference: WhatsApp or direct domain (use official)
- Color hex codes for accent (if gold used: #D4AF37; if white: #FFFFFF; background: #141823 or similar approved dark tone)

**Non-Generative (Post-Production Assembly):**
- Overlay aight's official wordmark on generated background if generation does not include it with sufficient fidelity.
- If generated prices are unreadable or misaligned, replace with vector text at exact sizes and positions.
- Manual spell-check and proofing of all supporting text.
- Export at 1080×1350 px (4:5), then verify legibility at 300px width (mobile preview).

---

### AUDIO_AND_EDIT

**Not applicable for a static poster.** 

If this poster is repurposed for a video (e.g., 15-second Instagram Reel with animated price reveal), consider:
- Subtle ambient sound or a single clean tone (no music; aligns with institutional brand).
- Price numbers animate in sequentially or expand into frame, with a voiceover: "Image generation at ₹9. Video generation at ₹99. Aight."
- Duration: 3 seconds for price reveal, with 2-second hold and 2-second call-to-action (contact/website URL).

---

### FAILURE_PREVENTION

**High-Risk Failure Modes:**

1. **Prices illegible on mobile:** Mitigation—ensure ₹9 and ₹99 are minimum 60pt equivalent at 300px width; test preview at that scale.

2. **Discount-retail visual tone:** Mitigation—avoid bright gradients, shadow effects, or ornamental graphics. Hold to monochromatic + single accent color. Trust typography entirely.

3. **Festive season feels cheap:** Mitigation—do not use cartoon or bright colors. Use gold only as a sophisticated accent (high-contrast, minimal use), not as pervasive fill. Retain institutional neutrality.

4. **Hierarchy unclear:** Mitigation—ensure prices occupy 40–50% of poster's height; all other text is subordinate in size and weight. No competing focal points.

5. **Contact information weak:** Mitigation—include "getaight.ai" or WhatsApp in readable size (min 12pt), positioned clearly at bottom. If WhatsApp, include a small icon or prefix label.

6. **Wordmark placement wrong:** Mitigation—verify aight's official logo specification and placement before generation; use deterministic overlay if generation misplaces it.

7. **Text cut off on rounded corners (mobile):** Mitigation—avoid placing critical text in top/bottom corners; provide 50px safe margin on all edges for mobile viewing.

**Testing Checklist:**
- [ ] Legible at 300px width (mobile preview scale).
- [ ] Prices immediately scannable (eyes land on ₹9 and ₹99 within 2 seconds).
- [ ] No color or tone reads as "discount retailer" (compare to institutional finance/SaaS imagery).
- [ ] Aight wordmark present and correctly positioned.
- [ ] All contact information accurate (getaight.ai, WhatsApp handle).
- [ ] Suitable for print at 300 DPI and web at 72 DPI (no quality loss).

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 poster confirmed.  
✅ **Commercial proposition:** ₹9 (image) and ₹99 (video) clearly displayed, immediately understandable.  
✅ **Tone:** Serious AI infrastructure/product company, not discount retail—achieved via spare typography and institutional color/layout choices.  
✅ **Design focus:** Typography and information hierarchy are primary tools; minimal supplementary graphics.  
✅ **Source:** All brand and product information sourced exclusively from https://getaight.ai.  
✅ **Single deliverable:** One poster, one concept—no alternatives.  
✅ **Festive season relevance:** Positioned as "abundance at control," aligns with Indian festive value proposition without garish visual cues.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources Used:**
- **https://getaight.ai** (website snapshot): Brand positioning, messaging tone, product offering (image and video generation), target audience (Indian businesses), brand values (transparency, domestic, founder-led support, cost control, no hidden fees).

**Canon Knowledge Library:** Not consulted. Brand and product information obtained solely from aight's official website per customer instruction.

**Key Brand Insights Applied:**
- Aight's self-positioning as "Where Indian businesses buy AI" informs tagline direction.
- Emphasis on "prepaid rupees," "domestic GST invoice," and "hard caps" translates to supporting copy: "Prepaid. Domestic. Transparent."
- Founder-led support philosophy (WhatsApp contact, no ticket queue) supports direct contact CTA.
- Merchant/counter metaphor in website copy informed visual shelf structure for prices.
- No glossy AI jargon; clean, legible infrastructure aesthetic.

---

**END OF PRODUCTION PACKAGE**

## MESSAGE_AND_INFORMATION_HIERARCHY
**Primary (Top ~25% of poster):**
Wordmark + festive seasonal marker
"Image + Video. Aight Rates."  
(or) "Generate. India-Ready."

**Secondary (Center block ~50%—THE SHELF):**
```
₹9      ₹99
Image   Video
```
With sub-lines:
- "Per image generation"
- "Per video generation"
- Or simply visual markers (icon or label)

**Supporting (Bottom ~25%):**
- Tagline reinforcing brand essence: "Control, Rupees, No Surprises" or "Prepaid. Domestic. Yours."
- Subtle reference to the merchant/counter metaphor: "Where Indian builders buy media AI"
- Minimal call-to-action: "getaight.ai" + WhatsApp handle or "Talk to us"

**Tone:** Confident, spare, legible at mobile scale.

---

### VISUAL_SYSTEM

**Typography (Execution-Level Guidance):**
- **Headings:** Geometric sans-serif, high contrast, bold weight (Aight's aesthetic reads modern-infrastructure, not playful). Recommend: Inter Black, IBM Plex Sans Bold, or equivalent clean sans.
- **Prices:** XL, dominant, set in a distinct weight or color to ensure immediate focus.
- **Supporting text:** Light/regular weight, same typeface family, generous line spacing for clarity.

**Color Palette:**
- **Primary:** Deep, professional background (charcoal, navy, or near-black) to establish premium infrastructure feel.
- **Accent:** Single accent color for prices—either warm gold/orange (festive, prosperity, auspicious in Indian context) or crisp white/cream for maximum contrast. Avoid bright neons; maintain institutional credibility.
- **Alternative:** Minimal color—prices in a single bold color (gold or white), rest monochromatic.

**Layout:**
- Full-bleed background, minimal margins.
- Vertical rhythm: top section (10%), price shelf (50%), bottom section (40%).
- Prices centered, substantial whitespace around them (breathe the hierarchy).
- Clean baseline grid; every line intentional.

**Visual Assets:**
- No illustrations or decorative icons beyond minimal geometric markers (e.g., a thin line separating sections, a small merchant-counter reference).
- Festive element (if needed): A subtle pattern or texture in the background, or a single embellishment in the bottom corner—but keep it refined, not garish.
- Aight wordmark placed clearly (likely top-left or top-center).

---

### PRODUCTION_RECIPE

**Input Specification:**
- Canvas: 1080×1350 px (4:5 aspect ratio, standard for Instagram Stories/Reels, mobile ads, printable at 300 DPI as 14.4" × 18")
- 300 DPI output for print; 72 DPI for web.

**Build Process:**
1. **Base layer:** Solid background color (charcoal or navy, RGB: 20, 24, 35 or similar deep tone).
2. **Typography layer:** 
   - Aight wordmark (top, 12% from top).
   - Festive/seasonal marker (small text or emoji, e.g., "This Festive Season" or similar, 8pt).
   - Main headline (e.g., "Generate. Get Rates." centered, 48–60pt bold).
3. **Price shelf (center):**
   - Two columns: left "₹9 Image", right "₹99 Video".
   - Price numerals: 120–150pt, bold, accent color (gold #D4AF37 or white #FFFFFF on dark ground).
   - Sub-labels: 14–18pt, light gray or white, supporting text.
4. **Bottom section:**
   - Tagline: 16–20pt, light weight.
   - Contact line: "getaight.ai" or "WhatsApp: [link]", minimal size.
5. **Refinement:** Adjust kerning, leading, and whitespace for premium feel; ensure legibility at 300px width (mobile preview).

**Design Notes:**
- Avoid centered-text softness; use ranged left/right alignment or strong centering for hierarchy.
- Leave generous whitespace; cramped = discount retail.
- No drop shadows, gradients, or effects unless absolutely necessary.

---

### GENERATION_PROMPTS

**Final Executable Prompt for Image Generation:**

> Create a premium 4:5 portrait promotional poster for an AI infrastructure company. 
> 
> Background: Solid deep charcoal (almost black), professional and institutional. No gradients or texture.
>
> Top section (10% of height): Place the wordmark "aight" in crisp white, sans-serif, modern style. Below it, small text in light gray: "This Festive Season".
>
> Center section (50% of height): Large, dominant headline text in clean white sans-serif: "Generate at Aight Rates." Beneath this, two large pricing blocks side by side, separated by whitespace:
> - Left: The symbol "₹9" in very large, bold typeface (120pt equivalent, dark gold or bright white), with supporting text "Per Image" underneath in small light gray text.
> - Right: The symbol "₹99" in the same large, bold typeface, with supporting text "Per Video" underneath in matching gray.
>
> Bottom section (40% of height): 
> - Centered, modest tagline in light gray: "Prepaid in Rupees. Domestic GST. Control Your Spend."
> - Below that, a line in white: "getaight.ai"
> - Very small text: "Where Indian businesses buy media AI"
>
> Overall aesthetic: Institutional, transparent, serious infrastructure feel. Maximum legibility on mobile (minimum 300px wide). Use only clean sans-serif typography (no serifs, no scripts). No illustrations, icons, or decorative elements. Minimal whitespace around prices to emphasize hierarchy. Print-ready, professional, premium positioning.

**Alternative Tighter Prompt (if strict generation control needed):**

> Premium dark poster, 4:5 format. Background: charcoal black. Top: "aight" wordmark (white, sans-serif). Center: Two large prices, ₹9 and ₹99, bold white text on black, with labels "Image" and "Video" in gray below. Bottom: "getaight.ai" and tagline "Domestic. Transparent. For Builders." Typography-led design, no illustrations. Festive season framing implicit in abundance messaging. Institutional tone.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Deterministic (Fixed, Non-Generated):**
- Exact pricing figures: ₹9 and ₹99 (must not be altered by generation)
- Aight wordmark/logo (use official brand asset; do not regenerate)
- Website URL: getaight.ai (exact spelling, no variation)
- Contact method reference: WhatsApp or direct domain (use official)
- Color hex codes for accent (if gold used: #D4AF37; if white: #FFFFFF; background: #141823 or similar approved dark tone)

**Non-Generative (Post-Production Assembly):**
- Overlay aight's official wordmark on generated background if generation does not include it with sufficient fidelity.
- If generated prices are unreadable or misaligned, replace with vector text at exact sizes and positions.
- Manual spell-check and proofing of all supporting text.
- Export at 1080×1350 px (4:5), then verify legibility at 300px width (mobile preview).

---

### AUDIO_AND_EDIT

**Not applicable for a static poster.** 

If this poster is repurposed for a video (e.g., 15-second Instagram Reel with animated price reveal), consider:
- Subtle ambient sound or a single clean tone (no music; aligns with institutional brand).
- Price numbers animate in sequentially or expand into frame, with a voiceover: "Image generation at ₹9. Video generation at ₹99. Aight."
- Duration: 3 seconds for price reveal, with 2-second hold and 2-second call-to-action (contact/website URL).

---

### FAILURE_PREVENTION

**High-Risk Failure Modes:**

1. **Prices illegible on mobile:** Mitigation—ensure ₹9 and ₹99 are minimum 60pt equivalent at 300px width; test preview at that scale.

2. **Discount-retail visual tone:** Mitigation—avoid bright gradients, shadow effects, or ornamental graphics. Hold to monochromatic + single accent color. Trust typography entirely.

3. **Festive season feels cheap:** Mitigation—do not use cartoon or bright colors. Use gold only as a sophisticated accent (high-contrast, minimal use), not as pervasive fill. Retain institutional neutrality.

4. **Hierarchy unclear:** Mitigation—ensure prices occupy 40–50% of poster's height; all other text is subordinate in size and weight. No competing focal points.

5. **Contact information weak:** Mitigation—include "getaight.ai" or WhatsApp in readable size (min 12pt), positioned clearly at bottom. If WhatsApp, include a small icon or prefix label.

6. **Wordmark placement wrong:** Mitigation—verify aight's official logo specification and placement before generation; use deterministic overlay if generation misplaces it.

7. **Text cut off on rounded corners (mobile):** Mitigation—avoid placing critical text in top/bottom corners; provide 50px safe margin on all edges for mobile viewing.

**Testing Checklist:**
- [ ] Legible at 300px width (mobile preview scale).
- [ ] Prices immediately scannable (eyes land on ₹9 and ₹99 within 2 seconds).
- [ ] No color or tone reads as "discount retailer" (compare to institutional finance/SaaS imagery).
- [ ] Aight wordmark present and correctly positioned.
- [ ] All contact information accurate (getaight.ai, WhatsApp handle).
- [ ] Suitable for print at 300 DPI and web at 72 DPI (no quality loss).

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 poster confirmed.  
✅ **Commercial proposition:** ₹9 (image) and ₹99 (video) clearly displayed, immediately understandable.  
✅ **Tone:** Serious AI infrastructure/product company, not discount retail—achieved via spare typography and institutional color/layout choices.  
✅ **Design focus:** Typography and information hierarchy are primary tools; minimal supplementary graphics.  
✅ **Source:** All brand and product information sourced exclusively from https://getaight.ai.  
✅ **Single deliverable:** One poster, one concept—no alternatives.  
✅ **Festive season relevance:** Positioned as "abundance at control," aligns with Indian festive value proposition without garish visual cues.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources Used:**
- **https://getaight.ai** (website snapshot): Brand positioning, messaging tone, product offering (image and video generation), target audience (Indian businesses), brand values (transparency, domestic, founder-led support, cost control, no hidden fees).

**Canon Knowledge Library:** Not consulted. Brand and product information obtained solely from aight's official website per customer instruction.

**Key Brand Insights Applied:**
- Aight's self-positioning as "Where Indian businesses buy AI" informs tagline direction.
- Emphasis on "prepaid rupees," "domestic GST invoice," and "hard caps" translates to supporting copy: "Prepaid. Domestic. Transparent."
- Founder-led support philosophy (WhatsApp contact, no ticket queue) supports direct contact CTA.
- Merchant/counter metaphor in website copy informed visual shelf structure for prices.
- No glossy AI jargon; clean, legible infrastructure aesthetic.

---

**END OF PRODUCTION PACKAGE**

## VISUAL_SYSTEM
**Typography (Execution-Level Guidance):**
- **Headings:** Geometric sans-serif, high contrast, bold weight (Aight's aesthetic reads modern-infrastructure, not playful). Recommend: Inter Black, IBM Plex Sans Bold, or equivalent clean sans.
- **Prices:** XL, dominant, set in a distinct weight or color to ensure immediate focus.
- **Supporting text:** Light/regular weight, same typeface family, generous line spacing for clarity.

**Color Palette:**
- **Primary:** Deep, professional background (charcoal, navy, or near-black) to establish premium infrastructure feel.
- **Accent:** Single accent color for prices—either warm gold/orange (festive, prosperity, auspicious in Indian context) or crisp white/cream for maximum contrast. Avoid bright neons; maintain institutional credibility.
- **Alternative:** Minimal color—prices in a single bold color (gold or white), rest monochromatic.

**Layout:**
- Full-bleed background, minimal margins.
- Vertical rhythm: top section (10%), price shelf (50%), bottom section (40%).
- Prices centered, substantial whitespace around them (breathe the hierarchy).
- Clean baseline grid; every line intentional.

**Visual Assets:**
- No illustrations or decorative icons beyond minimal geometric markers (e.g., a thin line separating sections, a small merchant-counter reference).
- Festive element (if needed): A subtle pattern or texture in the background, or a single embellishment in the bottom corner—but keep it refined, not garish.
- Aight wordmark placed clearly (likely top-left or top-center).

---

### PRODUCTION_RECIPE

**Input Specification:**
- Canvas: 1080×1350 px (4:5 aspect ratio, standard for Instagram Stories/Reels, mobile ads, printable at 300 DPI as 14.4" × 18")
- 300 DPI output for print; 72 DPI for web.

**Build Process:**
1. **Base layer:** Solid background color (charcoal or navy, RGB: 20, 24, 35 or similar deep tone).
2. **Typography layer:** 
   - Aight wordmark (top, 12% from top).
   - Festive/seasonal marker (small text or emoji, e.g., "This Festive Season" or similar, 8pt).
   - Main headline (e.g., "Generate. Get Rates." centered, 48–60pt bold).
3. **Price shelf (center):**
   - Two columns: left "₹9 Image", right "₹99 Video".
   - Price numerals: 120–150pt, bold, accent color (gold #D4AF37 or white #FFFFFF on dark ground).
   - Sub-labels: 14–18pt, light gray or white, supporting text.
4. **Bottom section:**
   - Tagline: 16–20pt, light weight.
   - Contact line: "getaight.ai" or "WhatsApp: [link]", minimal size.
5. **Refinement:** Adjust kerning, leading, and whitespace for premium feel; ensure legibility at 300px width (mobile preview).

**Design Notes:**
- Avoid centered-text softness; use ranged left/right alignment or strong centering for hierarchy.
- Leave generous whitespace; cramped = discount retail.
- No drop shadows, gradients, or effects unless absolutely necessary.

---

### GENERATION_PROMPTS

**Final Executable Prompt for Image Generation:**

> Create a premium 4:5 portrait promotional poster for an AI infrastructure company. 
> 
> Background: Solid deep charcoal (almost black), professional and institutional. No gradients or texture.
>
> Top section (10% of height): Place the wordmark "aight" in crisp white, sans-serif, modern style. Below it, small text in light gray: "This Festive Season".
>
> Center section (50% of height): Large, dominant headline text in clean white sans-serif: "Generate at Aight Rates." Beneath this, two large pricing blocks side by side, separated by whitespace:
> - Left: The symbol "₹9" in very large, bold typeface (120pt equivalent, dark gold or bright white), with supporting text "Per Image" underneath in small light gray text.
> - Right: The symbol "₹99" in the same large, bold typeface, with supporting text "Per Video" underneath in matching gray.
>
> Bottom section (40% of height): 
> - Centered, modest tagline in light gray: "Prepaid in Rupees. Domestic GST. Control Your Spend."
> - Below that, a line in white: "getaight.ai"
> - Very small text: "Where Indian businesses buy media AI"
>
> Overall aesthetic: Institutional, transparent, serious infrastructure feel. Maximum legibility on mobile (minimum 300px wide). Use only clean sans-serif typography (no serifs, no scripts). No illustrations, icons, or decorative elements. Minimal whitespace around prices to emphasize hierarchy. Print-ready, professional, premium positioning.

**Alternative Tighter Prompt (if strict generation control needed):**

> Premium dark poster, 4:5 format. Background: charcoal black. Top: "aight" wordmark (white, sans-serif). Center: Two large prices, ₹9 and ₹99, bold white text on black, with labels "Image" and "Video" in gray below. Bottom: "getaight.ai" and tagline "Domestic. Transparent. For Builders." Typography-led design, no illustrations. Festive season framing implicit in abundance messaging. Institutional tone.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Deterministic (Fixed, Non-Generated):**
- Exact pricing figures: ₹9 and ₹99 (must not be altered by generation)
- Aight wordmark/logo (use official brand asset; do not regenerate)
- Website URL: getaight.ai (exact spelling, no variation)
- Contact method reference: WhatsApp or direct domain (use official)
- Color hex codes for accent (if gold used: #D4AF37; if white: #FFFFFF; background: #141823 or similar approved dark tone)

**Non-Generative (Post-Production Assembly):**
- Overlay aight's official wordmark on generated background if generation does not include it with sufficient fidelity.
- If generated prices are unreadable or misaligned, replace with vector text at exact sizes and positions.
- Manual spell-check and proofing of all supporting text.
- Export at 1080×1350 px (4:5), then verify legibility at 300px width (mobile preview).

---

### AUDIO_AND_EDIT

**Not applicable for a static poster.** 

If this poster is repurposed for a video (e.g., 15-second Instagram Reel with animated price reveal), consider:
- Subtle ambient sound or a single clean tone (no music; aligns with institutional brand).
- Price numbers animate in sequentially or expand into frame, with a voiceover: "Image generation at ₹9. Video generation at ₹99. Aight."
- Duration: 3 seconds for price reveal, with 2-second hold and 2-second call-to-action (contact/website URL).

---

### FAILURE_PREVENTION

**High-Risk Failure Modes:**

1. **Prices illegible on mobile:** Mitigation—ensure ₹9 and ₹99 are minimum 60pt equivalent at 300px width; test preview at that scale.

2. **Discount-retail visual tone:** Mitigation—avoid bright gradients, shadow effects, or ornamental graphics. Hold to monochromatic + single accent color. Trust typography entirely.

3. **Festive season feels cheap:** Mitigation—do not use cartoon or bright colors. Use gold only as a sophisticated accent (high-contrast, minimal use), not as pervasive fill. Retain institutional neutrality.

4. **Hierarchy unclear:** Mitigation—ensure prices occupy 40–50% of poster's height; all other text is subordinate in size and weight. No competing focal points.

5. **Contact information weak:** Mitigation—include "getaight.ai" or WhatsApp in readable size (min 12pt), positioned clearly at bottom. If WhatsApp, include a small icon or prefix label.

6. **Wordmark placement wrong:** Mitigation—verify aight's official logo specification and placement before generation; use deterministic overlay if generation misplaces it.

7. **Text cut off on rounded corners (mobile):** Mitigation—avoid placing critical text in top/bottom corners; provide 50px safe margin on all edges for mobile viewing.

**Testing Checklist:**
- [ ] Legible at 300px width (mobile preview scale).
- [ ] Prices immediately scannable (eyes land on ₹9 and ₹99 within 2 seconds).
- [ ] No color or tone reads as "discount retailer" (compare to institutional finance/SaaS imagery).
- [ ] Aight wordmark present and correctly positioned.
- [ ] All contact information accurate (getaight.ai, WhatsApp handle).
- [ ] Suitable for print at 300 DPI and web at 72 DPI (no quality loss).

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 poster confirmed.  
✅ **Commercial proposition:** ₹9 (image) and ₹99 (video) clearly displayed, immediately understandable.  
✅ **Tone:** Serious AI infrastructure/product company, not discount retail—achieved via spare typography and institutional color/layout choices.  
✅ **Design focus:** Typography and information hierarchy are primary tools; minimal supplementary graphics.  
✅ **Source:** All brand and product information sourced exclusively from https://getaight.ai.  
✅ **Single deliverable:** One poster, one concept—no alternatives.  
✅ **Festive season relevance:** Positioned as "abundance at control," aligns with Indian festive value proposition without garish visual cues.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources Used:**
- **https://getaight.ai** (website snapshot): Brand positioning, messaging tone, product offering (image and video generation), target audience (Indian businesses), brand values (transparency, domestic, founder-led support, cost control, no hidden fees).

**Canon Knowledge Library:** Not consulted. Brand and product information obtained solely from aight's official website per customer instruction.

**Key Brand Insights Applied:**
- Aight's self-positioning as "Where Indian businesses buy AI" informs tagline direction.
- Emphasis on "prepaid rupees," "domestic GST invoice," and "hard caps" translates to supporting copy: "Prepaid. Domestic. Transparent."
- Founder-led support philosophy (WhatsApp contact, no ticket queue) supports direct contact CTA.
- Merchant/counter metaphor in website copy informed visual shelf structure for prices.
- No glossy AI jargon; clean, legible infrastructure aesthetic.

---

**END OF PRODUCTION PACKAGE**

## PRODUCTION_RECIPE
**Input Specification:**
- Canvas: 1080×1350 px (4:5 aspect ratio, standard for Instagram Stories/Reels, mobile ads, printable at 300 DPI as 14.4" × 18")
- 300 DPI output for print; 72 DPI for web.

**Build Process:**
1. **Base layer:** Solid background color (charcoal or navy, RGB: 20, 24, 35 or similar deep tone).
2. **Typography layer:** 
   - Aight wordmark (top, 12% from top).
   - Festive/seasonal marker (small text or emoji, e.g., "This Festive Season" or similar, 8pt).
   - Main headline (e.g., "Generate. Get Rates." centered, 48–60pt bold).
3. **Price shelf (center):**
   - Two columns: left "₹9 Image", right "₹99 Video".
   - Price numerals: 120–150pt, bold, accent color (gold #D4AF37 or white #FFFFFF on dark ground).
   - Sub-labels: 14–18pt, light gray or white, supporting text.
4. **Bottom section:**
   - Tagline: 16–20pt, light weight.
   - Contact line: "getaight.ai" or "WhatsApp: [link]", minimal size.
5. **Refinement:** Adjust kerning, leading, and whitespace for premium feel; ensure legibility at 300px width (mobile preview).

**Design Notes:**
- Avoid centered-text softness; use ranged left/right alignment or strong centering for hierarchy.
- Leave generous whitespace; cramped = discount retail.
- No drop shadows, gradients, or effects unless absolutely necessary.

---

### GENERATION_PROMPTS

**Final Executable Prompt for Image Generation:**

> Create a premium 4:5 portrait promotional poster for an AI infrastructure company. 
> 
> Background: Solid deep charcoal (almost black), professional and institutional. No gradients or texture.
>
> Top section (10% of height): Place the wordmark "aight" in crisp white, sans-serif, modern style. Below it, small text in light gray: "This Festive Season".
>
> Center section (50% of height): Large, dominant headline text in clean white sans-serif: "Generate at Aight Rates." Beneath this, two large pricing blocks side by side, separated by whitespace:
> - Left: The symbol "₹9" in very large, bold typeface (120pt equivalent, dark gold or bright white), with supporting text "Per Image" underneath in small light gray text.
> - Right: The symbol "₹99" in the same large, bold typeface, with supporting text "Per Video" underneath in matching gray.
>
> Bottom section (40% of height): 
> - Centered, modest tagline in light gray: "Prepaid in Rupees. Domestic GST. Control Your Spend."
> - Below that, a line in white: "getaight.ai"
> - Very small text: "Where Indian businesses buy media AI"
>
> Overall aesthetic: Institutional, transparent, serious infrastructure feel. Maximum legibility on mobile (minimum 300px wide). Use only clean sans-serif typography (no serifs, no scripts). No illustrations, icons, or decorative elements. Minimal whitespace around prices to emphasize hierarchy. Print-ready, professional, premium positioning.

**Alternative Tighter Prompt (if strict generation control needed):**

> Premium dark poster, 4:5 format. Background: charcoal black. Top: "aight" wordmark (white, sans-serif). Center: Two large prices, ₹9 and ₹99, bold white text on black, with labels "Image" and "Video" in gray below. Bottom: "getaight.ai" and tagline "Domestic. Transparent. For Builders." Typography-led design, no illustrations. Festive season framing implicit in abundance messaging. Institutional tone.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Deterministic (Fixed, Non-Generated):**
- Exact pricing figures: ₹9 and ₹99 (must not be altered by generation)
- Aight wordmark/logo (use official brand asset; do not regenerate)
- Website URL: getaight.ai (exact spelling, no variation)
- Contact method reference: WhatsApp or direct domain (use official)
- Color hex codes for accent (if gold used: #D4AF37; if white: #FFFFFF; background: #141823 or similar approved dark tone)

**Non-Generative (Post-Production Assembly):**
- Overlay aight's official wordmark on generated background if generation does not include it with sufficient fidelity.
- If generated prices are unreadable or misaligned, replace with vector text at exact sizes and positions.
- Manual spell-check and proofing of all supporting text.
- Export at 1080×1350 px (4:5), then verify legibility at 300px width (mobile preview).

---

### AUDIO_AND_EDIT

**Not applicable for a static poster.** 

If this poster is repurposed for a video (e.g., 15-second Instagram Reel with animated price reveal), consider:
- Subtle ambient sound or a single clean tone (no music; aligns with institutional brand).
- Price numbers animate in sequentially or expand into frame, with a voiceover: "Image generation at ₹9. Video generation at ₹99. Aight."
- Duration: 3 seconds for price reveal, with 2-second hold and 2-second call-to-action (contact/website URL).

---

### FAILURE_PREVENTION

**High-Risk Failure Modes:**

1. **Prices illegible on mobile:** Mitigation—ensure ₹9 and ₹99 are minimum 60pt equivalent at 300px width; test preview at that scale.

2. **Discount-retail visual tone:** Mitigation—avoid bright gradients, shadow effects, or ornamental graphics. Hold to monochromatic + single accent color. Trust typography entirely.

3. **Festive season feels cheap:** Mitigation—do not use cartoon or bright colors. Use gold only as a sophisticated accent (high-contrast, minimal use), not as pervasive fill. Retain institutional neutrality.

4. **Hierarchy unclear:** Mitigation—ensure prices occupy 40–50% of poster's height; all other text is subordinate in size and weight. No competing focal points.

5. **Contact information weak:** Mitigation—include "getaight.ai" or WhatsApp in readable size (min 12pt), positioned clearly at bottom. If WhatsApp, include a small icon or prefix label.

6. **Wordmark placement wrong:** Mitigation—verify aight's official logo specification and placement before generation; use deterministic overlay if generation misplaces it.

7. **Text cut off on rounded corners (mobile):** Mitigation—avoid placing critical text in top/bottom corners; provide 50px safe margin on all edges for mobile viewing.

**Testing Checklist:**
- [ ] Legible at 300px width (mobile preview scale).
- [ ] Prices immediately scannable (eyes land on ₹9 and ₹99 within 2 seconds).
- [ ] No color or tone reads as "discount retailer" (compare to institutional finance/SaaS imagery).
- [ ] Aight wordmark present and correctly positioned.
- [ ] All contact information accurate (getaight.ai, WhatsApp handle).
- [ ] Suitable for print at 300 DPI and web at 72 DPI (no quality loss).

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 poster confirmed.  
✅ **Commercial proposition:** ₹9 (image) and ₹99 (video) clearly displayed, immediately understandable.  
✅ **Tone:** Serious AI infrastructure/product company, not discount retail—achieved via spare typography and institutional color/layout choices.  
✅ **Design focus:** Typography and information hierarchy are primary tools; minimal supplementary graphics.  
✅ **Source:** All brand and product information sourced exclusively from https://getaight.ai.  
✅ **Single deliverable:** One poster, one concept—no alternatives.  
✅ **Festive season relevance:** Positioned as "abundance at control," aligns with Indian festive value proposition without garish visual cues.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources Used:**
- **https://getaight.ai** (website snapshot): Brand positioning, messaging tone, product offering (image and video generation), target audience (Indian businesses), brand values (transparency, domestic, founder-led support, cost control, no hidden fees).

**Canon Knowledge Library:** Not consulted. Brand and product information obtained solely from aight's official website per customer instruction.

**Key Brand Insights Applied:**
- Aight's self-positioning as "Where Indian businesses buy AI" informs tagline direction.
- Emphasis on "prepaid rupees," "domestic GST invoice," and "hard caps" translates to supporting copy: "Prepaid. Domestic. Transparent."
- Founder-led support philosophy (WhatsApp contact, no ticket queue) supports direct contact CTA.
- Merchant/counter metaphor in website copy informed visual shelf structure for prices.
- No glossy AI jargon; clean, legible infrastructure aesthetic.

---

**END OF PRODUCTION PACKAGE**

## GENERATION_PROMPTS
**Final Executable Prompt for Image Generation:**

> Create a premium 4:5 portrait promotional poster for an AI infrastructure company. 
> 
> Background: Solid deep charcoal (almost black), professional and institutional. No gradients or texture.
>
> Top section (10% of height): Place the wordmark "aight" in crisp white, sans-serif, modern style. Below it, small text in light gray: "This Festive Season".
>
> Center section (50% of height): Large, dominant headline text in clean white sans-serif: "Generate at Aight Rates." Beneath this, two large pricing blocks side by side, separated by whitespace:
> - Left: The symbol "₹9" in very large, bold typeface (120pt equivalent, dark gold or bright white), with supporting text "Per Image" underneath in small light gray text.
> - Right: The symbol "₹99" in the same large, bold typeface, with supporting text "Per Video" underneath in matching gray.
>
> Bottom section (40% of height): 
> - Centered, modest tagline in light gray: "Prepaid in Rupees. Domestic GST. Control Your Spend."
> - Below that, a line in white: "getaight.ai"
> - Very small text: "Where Indian businesses buy media AI"
>
> Overall aesthetic: Institutional, transparent, serious infrastructure feel. Maximum legibility on mobile (minimum 300px wide). Use only clean sans-serif typography (no serifs, no scripts). No illustrations, icons, or decorative elements. Minimal whitespace around prices to emphasize hierarchy. Print-ready, professional, premium positioning.

**Alternative Tighter Prompt (if strict generation control needed):**

> Premium dark poster, 4:5 format. Background: charcoal black. Top: "aight" wordmark (white, sans-serif). Center: Two large prices, ₹9 and ₹99, bold white text on black, with labels "Image" and "Video" in gray below. Bottom: "getaight.ai" and tagline "Domestic. Transparent. For Builders." Typography-led design, no illustrations. Festive season framing implicit in abundance messaging. Institutional tone.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

**Deterministic (Fixed, Non-Generated):**
- Exact pricing figures: ₹9 and ₹99 (must not be altered by generation)
- Aight wordmark/logo (use official brand asset; do not regenerate)
- Website URL: getaight.ai (exact spelling, no variation)
- Contact method reference: WhatsApp or direct domain (use official)
- Color hex codes for accent (if gold used: #D4AF37; if white: #FFFFFF; background: #141823 or similar approved dark tone)

**Non-Generative (Post-Production Assembly):**
- Overlay aight's official wordmark on generated background if generation does not include it with sufficient fidelity.
- If generated prices are unreadable or misaligned, replace with vector text at exact sizes and positions.
- Manual spell-check and proofing of all supporting text.
- Export at 1080×1350 px (4:5), then verify legibility at 300px width (mobile preview).

---

### AUDIO_AND_EDIT

**Not applicable for a static poster.** 

If this poster is repurposed for a video (e.g., 15-second Instagram Reel with animated price reveal), consider:
- Subtle ambient sound or a single clean tone (no music; aligns with institutional brand).
- Price numbers animate in sequentially or expand into frame, with a voiceover: "Image generation at ₹9. Video generation at ₹99. Aight."
- Duration: 3 seconds for price reveal, with 2-second hold and 2-second call-to-action (contact/website URL).

---

### FAILURE_PREVENTION

**High-Risk Failure Modes:**

1. **Prices illegible on mobile:** Mitigation—ensure ₹9 and ₹99 are minimum 60pt equivalent at 300px width; test preview at that scale.

2. **Discount-retail visual tone:** Mitigation—avoid bright gradients, shadow effects, or ornamental graphics. Hold to monochromatic + single accent color. Trust typography entirely.

3. **Festive season feels cheap:** Mitigation—do not use cartoon or bright colors. Use gold only as a sophisticated accent (high-contrast, minimal use), not as pervasive fill. Retain institutional neutrality.

4. **Hierarchy unclear:** Mitigation—ensure prices occupy 40–50% of poster's height; all other text is subordinate in size and weight. No competing focal points.

5. **Contact information weak:** Mitigation—include "getaight.ai" or WhatsApp in readable size (min 12pt), positioned clearly at bottom. If WhatsApp, include a small icon or prefix label.

6. **Wordmark placement wrong:** Mitigation—verify aight's official logo specification and placement before generation; use deterministic overlay if generation misplaces it.

7. **Text cut off on rounded corners (mobile):** Mitigation—avoid placing critical text in top/bottom corners; provide 50px safe margin on all edges for mobile viewing.

**Testing Checklist:**
- [ ] Legible at 300px width (mobile preview scale).
- [ ] Prices immediately scannable (eyes land on ₹9 and ₹99 within 2 seconds).
- [ ] No color or tone reads as "discount retailer" (compare to institutional finance/SaaS imagery).
- [ ] Aight wordmark present and correctly positioned.
- [ ] All contact information accurate (getaight.ai, WhatsApp handle).
- [ ] Suitable for print at 300 DPI and web at 72 DPI (no quality loss).

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 poster confirmed.  
✅ **Commercial proposition:** ₹9 (image) and ₹99 (video) clearly displayed, immediately understandable.  
✅ **Tone:** Serious AI infrastructure/product company, not discount retail—achieved via spare typography and institutional color/layout choices.  
✅ **Design focus:** Typography and information hierarchy are primary tools; minimal supplementary graphics.  
✅ **Source:** All brand and product information sourced exclusively from https://getaight.ai.  
✅ **Single deliverable:** One poster, one concept—no alternatives.  
✅ **Festive season relevance:** Positioned as "abundance at control," aligns with Indian festive value proposition without garish visual cues.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources Used:**
- **https://getaight.ai** (website snapshot): Brand positioning, messaging tone, product offering (image and video generation), target audience (Indian businesses), brand values (transparency, domestic, founder-led support, cost control, no hidden fees).

**Canon Knowledge Library:** Not consulted. Brand and product information obtained solely from aight's official website per customer instruction.

**Key Brand Insights Applied:**
- Aight's self-positioning as "Where Indian businesses buy AI" informs tagline direction.
- Emphasis on "prepaid rupees," "domestic GST invoice," and "hard caps" translates to supporting copy: "Prepaid. Domestic. Transparent."
- Founder-led support philosophy (WhatsApp contact, no ticket queue) supports direct contact CTA.
- Merchant/counter metaphor in website copy informed visual shelf structure for prices.
- No glossy AI jargon; clean, legible infrastructure aesthetic.

---

**END OF PRODUCTION PACKAGE**

## DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS
**Deterministic (Fixed, Non-Generated):**
- Exact pricing figures: ₹9 and ₹99 (must not be altered by generation)
- Aight wordmark/logo (use official brand asset; do not regenerate)
- Website URL: getaight.ai (exact spelling, no variation)
- Contact method reference: WhatsApp or direct domain (use official)
- Color hex codes for accent (if gold used: #D4AF37; if white: #FFFFFF; background: #141823 or similar approved dark tone)

**Non-Generative (Post-Production Assembly):**
- Overlay aight's official wordmark on generated background if generation does not include it with sufficient fidelity.
- If generated prices are unreadable or misaligned, replace with vector text at exact sizes and positions.
- Manual spell-check and proofing of all supporting text.
- Export at 1080×1350 px (4:5), then verify legibility at 300px width (mobile preview).

---

### AUDIO_AND_EDIT

**Not applicable for a static poster.** 

If this poster is repurposed for a video (e.g., 15-second Instagram Reel with animated price reveal), consider:
- Subtle ambient sound or a single clean tone (no music; aligns with institutional brand).
- Price numbers animate in sequentially or expand into frame, with a voiceover: "Image generation at ₹9. Video generation at ₹99. Aight."
- Duration: 3 seconds for price reveal, with 2-second hold and 2-second call-to-action (contact/website URL).

---

### FAILURE_PREVENTION

**High-Risk Failure Modes:**

1. **Prices illegible on mobile:** Mitigation—ensure ₹9 and ₹99 are minimum 60pt equivalent at 300px width; test preview at that scale.

2. **Discount-retail visual tone:** Mitigation—avoid bright gradients, shadow effects, or ornamental graphics. Hold to monochromatic + single accent color. Trust typography entirely.

3. **Festive season feels cheap:** Mitigation—do not use cartoon or bright colors. Use gold only as a sophisticated accent (high-contrast, minimal use), not as pervasive fill. Retain institutional neutrality.

4. **Hierarchy unclear:** Mitigation—ensure prices occupy 40–50% of poster's height; all other text is subordinate in size and weight. No competing focal points.

5. **Contact information weak:** Mitigation—include "getaight.ai" or WhatsApp in readable size (min 12pt), positioned clearly at bottom. If WhatsApp, include a small icon or prefix label.

6. **Wordmark placement wrong:** Mitigation—verify aight's official logo specification and placement before generation; use deterministic overlay if generation misplaces it.

7. **Text cut off on rounded corners (mobile):** Mitigation—avoid placing critical text in top/bottom corners; provide 50px safe margin on all edges for mobile viewing.

**Testing Checklist:**
- [ ] Legible at 300px width (mobile preview scale).
- [ ] Prices immediately scannable (eyes land on ₹9 and ₹99 within 2 seconds).
- [ ] No color or tone reads as "discount retailer" (compare to institutional finance/SaaS imagery).
- [ ] Aight wordmark present and correctly positioned.
- [ ] All contact information accurate (getaight.ai, WhatsApp handle).
- [ ] Suitable for print at 300 DPI and web at 72 DPI (no quality loss).

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 poster confirmed.  
✅ **Commercial proposition:** ₹9 (image) and ₹99 (video) clearly displayed, immediately understandable.  
✅ **Tone:** Serious AI infrastructure/product company, not discount retail—achieved via spare typography and institutional color/layout choices.  
✅ **Design focus:** Typography and information hierarchy are primary tools; minimal supplementary graphics.  
✅ **Source:** All brand and product information sourced exclusively from https://getaight.ai.  
✅ **Single deliverable:** One poster, one concept—no alternatives.  
✅ **Festive season relevance:** Positioned as "abundance at control," aligns with Indian festive value proposition without garish visual cues.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources Used:**
- **https://getaight.ai** (website snapshot): Brand positioning, messaging tone, product offering (image and video generation), target audience (Indian businesses), brand values (transparency, domestic, founder-led support, cost control, no hidden fees).

**Canon Knowledge Library:** Not consulted. Brand and product information obtained solely from aight's official website per customer instruction.

**Key Brand Insights Applied:**
- Aight's self-positioning as "Where Indian businesses buy AI" informs tagline direction.
- Emphasis on "prepaid rupees," "domestic GST invoice," and "hard caps" translates to supporting copy: "Prepaid. Domestic. Transparent."
- Founder-led support philosophy (WhatsApp contact, no ticket queue) supports direct contact CTA.
- Merchant/counter metaphor in website copy informed visual shelf structure for prices.
- No glossy AI jargon; clean, legible infrastructure aesthetic.

---

**END OF PRODUCTION PACKAGE**

## FAILURE_PREVENTION
**High-Risk Failure Modes:**

1. **Prices illegible on mobile:** Mitigation—ensure ₹9 and ₹99 are minimum 60pt equivalent at 300px width; test preview at that scale.

2. **Discount-retail visual tone:** Mitigation—avoid bright gradients, shadow effects, or ornamental graphics. Hold to monochromatic + single accent color. Trust typography entirely.

3. **Festive season feels cheap:** Mitigation—do not use cartoon or bright colors. Use gold only as a sophisticated accent (high-contrast, minimal use), not as pervasive fill. Retain institutional neutrality.

4. **Hierarchy unclear:** Mitigation—ensure prices occupy 40–50% of poster's height; all other text is subordinate in size and weight. No competing focal points.

5. **Contact information weak:** Mitigation—include "getaight.ai" or WhatsApp in readable size (min 12pt), positioned clearly at bottom. If WhatsApp, include a small icon or prefix label.

6. **Wordmark placement wrong:** Mitigation—verify aight's official logo specification and placement before generation; use deterministic overlay if generation misplaces it.

7. **Text cut off on rounded corners (mobile):** Mitigation—avoid placing critical text in top/bottom corners; provide 50px safe margin on all edges for mobile viewing.

**Testing Checklist:**
- [ ] Legible at 300px width (mobile preview scale).
- [ ] Prices immediately scannable (eyes land on ₹9 and ₹99 within 2 seconds).
- [ ] No color or tone reads as "discount retailer" (compare to institutional finance/SaaS imagery).
- [ ] Aight wordmark present and correctly positioned.
- [ ] All contact information accurate (getaight.ai, WhatsApp handle).
- [ ] Suitable for print at 300 DPI and web at 72 DPI (no quality loss).

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 poster confirmed.  
✅ **Commercial proposition:** ₹9 (image) and ₹99 (video) clearly displayed, immediately understandable.  
✅ **Tone:** Serious AI infrastructure/product company, not discount retail—achieved via spare typography and institutional color/layout choices.  
✅ **Design focus:** Typography and information hierarchy are primary tools; minimal supplementary graphics.  
✅ **Source:** All brand and product information sourced exclusively from https://getaight.ai.  
✅ **Single deliverable:** One poster, one concept—no alternatives.  
✅ **Festive season relevance:** Positioned as "abundance at control," aligns with Indian festive value proposition without garish visual cues.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources Used:**
- **https://getaight.ai** (website snapshot): Brand positioning, messaging tone, product offering (image and video generation), target audience (Indian businesses), brand values (transparency, domestic, founder-led support, cost control, no hidden fees).

**Canon Knowledge Library:** Not consulted. Brand and product information obtained solely from aight's official website per customer instruction.

**Key Brand Insights Applied:**
- Aight's self-positioning as "Where Indian businesses buy AI" informs tagline direction.
- Emphasis on "prepaid rupees," "domestic GST invoice," and "hard caps" translates to supporting copy: "Prepaid. Domestic. Transparent."
- Founder-led support philosophy (WhatsApp contact, no ticket queue) supports direct contact CTA.
- Merchant/counter metaphor in website copy informed visual shelf structure for prices.
- No glossy AI jargon; clean, legible infrastructure aesthetic.

---

**END OF PRODUCTION PACKAGE**

## HARD_CONSTRAINT_CHECK
✅ **Format:** 4:5 poster confirmed.  
✅ **Commercial proposition:** ₹9 (image) and ₹99 (video) clearly displayed, immediately understandable.  
✅ **Tone:** Serious AI infrastructure/product company, not discount retail—achieved via spare typography and institutional color/layout choices.  
✅ **Design focus:** Typography and information hierarchy are primary tools; minimal supplementary graphics.  
✅ **Source:** All brand and product information sourced exclusively from https://getaight.ai.  
✅ **Single deliverable:** One poster, one concept—no alternatives.  
✅ **Festive season relevance:** Positioned as "abundance at control," aligns with Indian festive value proposition without garish visual cues.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources Used:**
- **https://getaight.ai** (website snapshot): Brand positioning, messaging tone, product offering (image and video generation), target audience (Indian businesses), brand values (transparency, domestic, founder-led support, cost control, no hidden fees).

**Canon Knowledge Library:** Not consulted. Brand and product information obtained solely from aight's official website per customer instruction.

**Key Brand Insights Applied:**
- Aight's self-positioning as "Where Indian businesses buy AI" informs tagline direction.
- Emphasis on "prepaid rupees," "domestic GST invoice," and "hard caps" translates to supporting copy: "Prepaid. Domestic. Transparent."
- Founder-led support philosophy (WhatsApp contact, no ticket queue) supports direct contact CTA.
- Merchant/counter metaphor in website copy informed visual shelf structure for prices.
- No glossy AI jargon; clean, legible infrastructure aesthetic.

---

**END OF PRODUCTION PACKAGE**

## GENERATE I11
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I12 — B02

Source key: E037-haiku-full-canon-B02-R3
Use frozen brief B02 from the top of this file.

## DELIVERABLE
One premium vertical promotional poster (4:5 aspect ratio) for Indian businesses, emphasizing aight's image and video generation API pricing during festive season.

---

## OBJECTIVE_INTERPRETATION
Present aight's media-generation pricing (₹9 image / ₹99 video) as a serious, accessible infrastructure solution for Indian businesses during peak festive buying season. The poster must signal quality, control and trust—core to aight's brand positioning ("AI, done right")—while making commercial terms immediately legible through typographic hierarchy rather than promotional noise.

---

## CORE_CREATIVE_IDEA
**Clean Duality**: Use stark typographic contrast to anchor two parallel propositions—image and video—as distinct product tiers within a single, unified platform narrative. The prices become an information product themselves, not a discount hook. White/cream space and generous margins enforce premium positioning; the festive season is signaled through warm color accent only, not decorative clutter.

**Insight from brand**: aight's messaging centers on transparency, control, and "the merchant's job"—getting the details right. The poster applies this: visible cost structure, no hidden terms, single clean invoice concept transposed to visual language.

---

## MESSAGE_AND_INFORMATION_HIERARCHY
**Primary (Visual anchor):**
- Image: ₹9 | Video: ₹99
- Sub-claim: "AI for your campaign. Prepaid. Clear."

**Secondary (Brand/proof):**
- Headline: "Build faster this season"
- Supporting line: "Image generation, video generation—one platform, one wallet, one GST invoice."

**Tertiary (Proof points):**
- "Used by Cypherock, RentOk, Ascend Foods"
- "Prepaid rupee wallet. Hard caps. No forex."

**Call-to-action:**
- "Talk to us on WhatsApp" or "getaight.ai"

**Hierarchy structure**: Price statement dominates the upper-middle section. Headline sits above. Brand proof and wallet benefit below. CTAssit at footer.

---

## VISUAL_SYSTEM
**Grid & Layout:**
- 4:5 vertical (poster standard)
- Single-column, centered axis
- Breathing room (margins ≥10% of canvas width)
- Two-step price reveal: Image/Video statement separates visually from supporting copy

**Typography:**
- **Headline** (Brand assertion): Bold sans-serif, 48–56pt, single line ("Build faster this season")
- **Price tier heads** ("Image", "Video"): 32–40pt, medium weight, uppercase or title case
- **Prices** (₹9 / ₹99): 64–80pt, bold display font or bold sans, positioned left-aligned under each tier head
- **Subheading & support**: 18–20pt, regular weight, line height 1.4–1.5 for legibility
- **Body/proof**: 14–16pt, regular, gray/muted tone
- **CTA**: 16–18pt, bold, accent color

**Color Palette:**
- **Base**: White/cream (main background)
- **Text**: Deep charcoal/black (primary), warm gray (secondary)
- **Accent**: Warm orange/saffron (20% opacity or solid, used only on CTA, divider line between image/video tiers, or subtle festive nod)
- **Rationale**: Festive season warmth appears only as a controlled accent, avoiding over-decoration. Maintains corporate sobriety.

**Visual Elements:**
- Thin horizontal divider line (accent color) separating image and video tiers
- Possible subtle dot/pillar pattern in footer (brand mark), minimal
- No photography; no AI-generated visuals in the design itself (reinforces controlled, deterministic approach)
- White space as primary design element

---

## PRODUCTION_RECIPE
**Format & specs:**
- Dimensions: 1000 × 1250 px (4:5, print-ready at 72 dpi for digital; scale to 3000 × 3750 for print production)
- File output: High-resolution PNG or PDF (vector preferred for text)
- Color mode: CMYK (print) or sRGB (digital)

**Construction sequence:**
1. Set up canvas at 4:5 ratio; establish margin safe zone (10% inset all sides)
2. Place headline ("Build faster this season") at top, centered, 48pt bold, black
3. Create upper section: "Image" (32pt) aligned left, with ₹9 (72pt bold) immediately below
4. Add thin horizontal divider line (accent saffron) spanning margin-to-margin
5. Create lower section: "Video" (32pt) aligned left, with ₹99 (72pt bold) immediately below
6. Insert supporting copy block below both tiers: "Prepaid. Clear. One platform, one wallet, one GST invoice." (18pt, regular, charcoal)
7. Add proof line: "Trusted by Cypherock, RentOk, Ascend Foods. No forex. Prepaid rupee wallet. Hard caps." (14pt, gray)
8. Footer: "Talk to us on WhatsApp | getaight.ai" (16pt bold, accent color CTA button or inline)
9. Apply 10% cream/warm white background (or pure white); soft shadow or border optional
10. Verify type contrast (WCAG AA minimum)

**Font recommendations:**
- **Display (prices)**: Inter Bold, Montserrat Bold, or similar contemporary sans-serif with strong weights
- **Headline & tier labels**: SF Pro Display or system sans-serif with mid-weights available
- **Body**: Inter, Roboto, or equivalent geometric sans (Indian markets often read sans-serif as more modern/trustworthy)

---

## GENERATION_PROMPTS
**For design software / manual construction (not generative image model):**

**Primary Prompt (for designer/typographer):**
> Create a premium vertical poster (4:5 ratio) for aight, an AI platform for Indian businesses. 
> 
> **Core hierarchy**: 
> - Top: Bold headline "Build faster this season" (48pt, black, centered)
> - Upper tier: Left-aligned word "Image" (32pt) with price ₹9 (72pt bold) directly below
> - Thin warm-orange divider line spanning full width
> - Lower tier: Left-aligned word "Video" (32pt) with price ₹99 (72pt bold) directly below
> - Below both: Supporting text "Prepaid. Clear. One platform, one wallet, one GST invoice." (18pt, regular)
> - Proof line: "Trusted by Cypherock, RentOk, Ascend Foods. No forex, no reverse-charge GST." (14pt, gray)
> - Footer CTA: "Talk to us on WhatsApp | getaight.ai" (16pt bold, warm orange or accent color)
>
> **Visual constraints**:
> - White/cream background
> - Deep charcoal text
> - Warm saffron/orange accent used only on divider, CTA, or subtle marks
> - 10% margins on all sides
> - No photography, no illustrations, no AI-style graphics
> - Typography and white space do all the work
> - Premium, serious tone (corporate AI platform, not retail discount)
> - Festive season atmosphere conveyed through warm accent color alone, not decoration
>
> **Mood**: Clean, trustworthy, structured. "The merchant's job done right."

**Alternative text variations** (for A/B testing if needed, but recommend single execution):
- Headline alt: "One wallet. Clear spend." (tighter brand fit)
- Supporting alt: "Image generation from ₹9. Video generation from ₹99. Prepaid rupees, one GST invoice."

---

## DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS
**Fully deterministic elements:**
- Prices (₹9 and ₹99) – fixed by customer brief
- Brand name: "aight"
- Proof customers: Cypherock, RentOk, Ascend Foods (from website)
- CTA: WhatsApp and getaight.ai (from website)
- Copy phrases: "Prepaid", "Hard caps", "One GST invoice", "No forex", "Rupee wallet" (from website messaging)
- Layout grid, margins, color palette (predefined above)
- Font families and weights (specified)

**No generative elements permitted:**
- Do not use any AI image generation for this poster itself
- All type, layout, and accent elements must be manually constructed
- Visual hierarchy must be typographically deliberate, not algorithmically suggested

---

## FAILURE_PREVENTION
| Risk | Mitigation |
|------|-----------|
| Prices appear cheapened or discount-oriented | Maintain 10% margins; use display typeface for prices (high prestige), not small/cramped type. Pair with premium support copy ("one GST invoice", "prepaid control"). |
| Festive season decoration feels kitschy | Restrict festive signaling to one warm accent color (saffron/orange) used sparingly on divider and CTA only. Avoid emoji, ornament, or seasonal imagery. |
| Type becomes hard to read on screen/in print | Test contrast ratios (WCAG AA: 4.5:1 minimum). Use deep charcoal on white/cream (meets 7:1). Gray secondary text still ≥4.5:1 on white. |
| Information hierarchy collapses | Enforce clear visual distance: 48pt headline → 32pt tier labels → 72pt prices → 18pt support → 14pt proof → 16pt CTA. No competing focal points. |
| Layout feels corporate-sterile, not inviting | Generous white space around prices and proof lines creates breathing room; warm accent on CTA and divider softens severity without compromise. |
| Poster does not resonate with Indian SMB audience | Use "rupees", "GST invoice", "WhatsApp" (from aight's own messaging). Proof customers are Indian-first. Text in English (standard for infrastructure products in India). |
| Price comparison is unclear | Physically separate image and video tiers with divider line. Align prices directly under category labels (no ambiguity). |

---

## HARD_CONSTRAINT_CHECK
✅ **One 4:5 poster** – Deliverable is single vertical poster, no alternatives.  
✅ **Prices immediately understandable** – ₹9 and ₹99 occupy dominant focal points (72pt bold display).  
✅ **Premium AI infrastructure tone** – No retail language, discount messaging, or decorative frivolity. Typography and white space dominate.  
✅ **Typography and hierarchy do the work** – No hero image, no illustration, no photography. Layout and type weight/size carry all meaning.  
✅ **Indian businesses as audience** – Copy includes "prepaid rupee wallet", "one GST invoice", "WhatsApp" CTA (aight's own channels).  
✅ **Festive season positioning** – Warm accent color (saffron/orange) as subtle nod; never overwrites brand seriousness.  
✅ **Only aight website (getaight.ai) used for information** – All copy, proof points, CTAs, and brand positioning extracted from website snapshot. No external sources.  
✅ **One production-ready solution** – No alternatives or concepts presented. Execution plan is complete and unambiguous.

---

## GENERATE I12
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I13 — B03

Source key: E037-haiku-full-canon-B03-R1
Use frozen brief B03 from the top of this file.

## DELIVERABLE
One premium 4:5 vertical still image for paid social and mobile display advertising. Product-forward, editorial in feel, no text overlay.

---

### OBJECTIVE_INTERPRETATION
Convince urban Indian consumers aged 22–35 that this is a premium, contemporary beverage choice—not mass-market soft drink. Signal refreshment, modernity, and connection to the mosambi (sweet lime) ingredient without resorting to decorative "Indian" tropes. Make the product glass unmistakably the visual anchor; let it anchor trust and desirability.

---

### CORE_CREATIVE_IDEA
**The Conversation Between Fruit and Refinement**

A single tall sparkling drink glass, half-filled with bright pale-amber liquid and visible carbonation, sits in neutral/cool light. One fresh mosambi fruit—cut or whole, unblemished, jewel-like—is positioned adjacent or slightly behind the glass, in sharp focus. Minimal negative space. No garnish clutter. The composition reveals:
- The drink's genuine colour and clarity (not artificial sweetness)
- The recognisable mosambi fruit as proof of ingredient authenticity
- Modern glassware suggesting premium positioning
- Restraint and craft, not volume or excess

The image reads as "sophisticated everyday" rather than "luxury spectacle" or "mass-market party."

---

### MESSAGE_AND_INFORMATION_HIERARCHY
1. **Primary:** The drink (glass, colour, carbonation) as the hero and trust signal
2. **Secondary:** The mosambi fruit as the cultural/ingredient anchor and proof of identity
3. **Tertiary:** Cleanliness, light, contemporary aesthetic (no text needed)

The mosambi does not illustrate the drink; it *validates* it. The drink's appearance sells the experience.

---

### VISUAL_SYSTEM

**Colour palette:**
- Pale warm gold to amber liquid (realistic mosambi sparkling water colour, not over-saturated)
- Cool whites, soft greys, or warm off-whites for background and negative space
- Mosambi: natural greens/yellows, matte and saturated
- No pattern, texture overload, or ornamental geometry

**Lighting:**
- Soft north-light or diffused directional light (no harsh shadows)
- Light enters the glass from above-left to show carbonation bubbles and liquid clarity
- Slight rim light on the glass edge to signal premium glassware
- Mosambi evenly lit, no hard shadows

**Composition:**
- Vertical 4:5 format: glass occupies the upper two-thirds (liquid filling roughly the middle zone), mosambi positioned lower-left or lower-right, slightly overlapping the glass base or sitting independently below
- Breathing room: 15–20% of frame is negative space (white or neutral)
- No clutter; no ice, no straw, no secondary objects

**Typography:**
- None in the image itself

---

### PRODUCTION_RECIPE

1. **Set dressing:** Clean white or pale grey seamless background (paper or painted wall). Minimal reflector fill; key light from above at 45°, soft diffusion.

2. **Glassware:** Tall, refined glass (straight or very slightly tapered). No branding visible. Fill with prepared mosambi sparkling water (or craft a visually identical mixture: pale golden sparkling water + mosambi juice or food colouring to exact the right tone). Ensure carbonation is visible; shoot soon after preparation.

3. **Fruit:** One fresh mosambi, unblemished. Shoot it whole and in-focus adjacent to the glass. Optional: one cross-section showing interior, placed nearby. Keep skin natural; do not over-oil or polish.

4. **Camera position:** Slightly above tabletop height (15–20° angle down); centred on the glass, mosambi in secondary focus zone.

5. **Post-production:** Minimal retouching. Correct exposure and colour balance to ensure the liquid reads as fresh and natural, not artificial or oversaturated. Sharpen the fruit. Leave natural skin texture on the mosambi. Slight vignette acceptable to draw eye to centre. Crop to exact 4:5.

---

### GENERATION_PROMPTS

**Final execution prompt:**

*A 4:5 vertical premium product photograph of a tall glass containing pale golden sparkling mosambi (sweet lime) water, carbonation bubbles clearly visible, positioned in the upper-centre portion of the frame. One fresh, whole mosambi fruit, matte-skinned, green-yellow, sits in sharp focus to the lower left of the glass base, slightly overlapped by the glass edge. Background is cool white or soft grey, seamless and empty. Soft diffused daylight from above illuminates the glass rim and liquid clarity. The fruit is naturally lit with no shiny oil. No text, no garnish, no ice, no secondary objects. Minimal negative space. Photography style: editorial, refined, contemporary. Colour grading: warm gold for the liquid, true greens and yellows for the fruit. Sharp, clean, modern. High-end beverage advertising aesthetic, not mass-market.*

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Mosambi fruit reference image(s):** Source one or two clear photographs of fresh mosambi from a library or supplier to ensure the model understands the fruit's exact appearance (colour, skin texture, size relative to the glass).
- **Glass reference:** Provide an image of the target glassware (tall, refined, minimalist—e.g., a simple tumbler or highball-style glass) to anchor the generation.
- **Colour reference:** Supply a swatch or sample image of the target liquid colour (pale golden amber) to guide hue.

These references act as visual briefs; they do not become part of the final image.

---

### AUDIO_AND_EDIT

Not applicable. This is a still image for social and mobile display.

---

### FAILURE_PREVENTION

**Failure modes and guardrails:**

1. **Overdesigned/cluttered image:** If the generation adds garnish, secondary fruit, condensation droplets, or a busy background, regenerate with explicit instruction: "Minimal. Nothing but the glass, the drink, and one mosambi fruit. Empty background. No clutter."

2. **Artificial or neon liquid colour:** If the liquid appears too bright, over-saturated, or fluorescent, request: "The sparkling water should be pale warm gold, natural-looking, not artificially bright. Like fresh pressed mosambi juice, not candy."

3. **Mosambi unrecognisable:** If the fruit looks generic or wrong, supply the reference image and request: "The fruit is a mosambi—pale yellow-green, round, thin skin, citrus. Match the provided reference image exactly."

4. **Text or branding creep:** If the model adds a product label, text, or brand mark, explicitly state: "No text. No labels. No branding visible. Image only."

5. **Wrong aspect ratio:** Ensure the final crop is exactly 4:5 (vertical, 1000 × 1250 pixels for digital use, or to client spec).

6. **Cheap or generic aesthetic:** If the image reads as a mass-market soft drink ad (gaudy, plastic, lifestyle-heavy), regenerate with: "Premium, editorial aesthetic. Refined simplicity. This is a contemporary craft beverage, not a mass-market product. Minimalist composition. Think luxury sparkling water or premium juice, not cola."

7. **Wrong lighting:** If shadows are harsh or the glass looks opaque, request: "Soft, diffused light. The glass and liquid must be crystal clear and luminous. Show the carbonation. Rim light on the glassware to emphasise premium quality."

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 vertical  
✅ **Product as hero:** Drink glass is the unmistakable focal point  
✅ **Mosambi included:** Fruit present and recognisable  
✅ **No clichéd "Indian" visual shorthand:** No flags, patterns, Taj Mahal, peacocks, or decorative geometry  
✅ **Sophisticated, not cheap:** Minimal, editorial, refined aesthetic; premium glassware; clean light  
✅ **Refreshing & contemporary:** Cool light, visible carbonation, modern composition  
✅ **Culturally familiar yet contemporary:** Mosambi is recognisable to the target audience and grounds the product in Indian citrus tradition; the execution is globally contemporary  
✅ **No celebrity:** None present  
✅ **No external website:** No links, QR codes, or URLs  
✅ **No text overlay:** Image is self-sufficient  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Canon sources used:**

1. **Ogilvy on Advertising, Ch. 2: "Make the Product the Hero"** (ACCEPTED)  
   - Application: Centring the glass and mosambi fruit as the unmistakable hero; rejecting decorative or lifestyle-heavy framing.

2. **Samara, *Making and Breaking the Grid*, Ch. 1: "Negative Space as Shape"** (ACCEPTED)  
   - Application: Treating empty space (white/grey background) as a compositional element of equal importance; breathing room in a 4:5 vertical format.

3. **Dwyer & Patel, *Cinema India*, Ch. 4: "Cultural Construction of Meaning" and related Q&A** (ACCEPTED)  
   - Application: Understanding that cultural specificity (mosambi) need not rely on text or ornamental shorthand; authentic presence of the ingredient itself communicates identity. Avoiding cliché by trusting the object's own meaning rather than layering decorative "Indian-ness."

**External websites:** None consulted or required.

---

**Ready for creative execution.**

## OBJECTIVE_INTERPRETATION
Convince urban Indian consumers aged 22–35 that this is a premium, contemporary beverage choice—not mass-market soft drink. Signal refreshment, modernity, and connection to the mosambi (sweet lime) ingredient without resorting to decorative "Indian" tropes. Make the product glass unmistakably the visual anchor; let it anchor trust and desirability.

---

### CORE_CREATIVE_IDEA
**The Conversation Between Fruit and Refinement**

A single tall sparkling drink glass, half-filled with bright pale-amber liquid and visible carbonation, sits in neutral/cool light. One fresh mosambi fruit—cut or whole, unblemished, jewel-like—is positioned adjacent or slightly behind the glass, in sharp focus. Minimal negative space. No garnish clutter. The composition reveals:
- The drink's genuine colour and clarity (not artificial sweetness)
- The recognisable mosambi fruit as proof of ingredient authenticity
- Modern glassware suggesting premium positioning
- Restraint and craft, not volume or excess

The image reads as "sophisticated everyday" rather than "luxury spectacle" or "mass-market party."

---

### MESSAGE_AND_INFORMATION_HIERARCHY
1. **Primary:** The drink (glass, colour, carbonation) as the hero and trust signal
2. **Secondary:** The mosambi fruit as the cultural/ingredient anchor and proof of identity
3. **Tertiary:** Cleanliness, light, contemporary aesthetic (no text needed)

The mosambi does not illustrate the drink; it *validates* it. The drink's appearance sells the experience.

---

### VISUAL_SYSTEM

**Colour palette:**
- Pale warm gold to amber liquid (realistic mosambi sparkling water colour, not over-saturated)
- Cool whites, soft greys, or warm off-whites for background and negative space
- Mosambi: natural greens/yellows, matte and saturated
- No pattern, texture overload, or ornamental geometry

**Lighting:**
- Soft north-light or diffused directional light (no harsh shadows)
- Light enters the glass from above-left to show carbonation bubbles and liquid clarity
- Slight rim light on the glass edge to signal premium glassware
- Mosambi evenly lit, no hard shadows

**Composition:**
- Vertical 4:5 format: glass occupies the upper two-thirds (liquid filling roughly the middle zone), mosambi positioned lower-left or lower-right, slightly overlapping the glass base or sitting independently below
- Breathing room: 15–20% of frame is negative space (white or neutral)
- No clutter; no ice, no straw, no secondary objects

**Typography:**
- None in the image itself

---

### PRODUCTION_RECIPE

1. **Set dressing:** Clean white or pale grey seamless background (paper or painted wall). Minimal reflector fill; key light from above at 45°, soft diffusion.

2. **Glassware:** Tall, refined glass (straight or very slightly tapered). No branding visible. Fill with prepared mosambi sparkling water (or craft a visually identical mixture: pale golden sparkling water + mosambi juice or food colouring to exact the right tone). Ensure carbonation is visible; shoot soon after preparation.

3. **Fruit:** One fresh mosambi, unblemished. Shoot it whole and in-focus adjacent to the glass. Optional: one cross-section showing interior, placed nearby. Keep skin natural; do not over-oil or polish.

4. **Camera position:** Slightly above tabletop height (15–20° angle down); centred on the glass, mosambi in secondary focus zone.

5. **Post-production:** Minimal retouching. Correct exposure and colour balance to ensure the liquid reads as fresh and natural, not artificial or oversaturated. Sharpen the fruit. Leave natural skin texture on the mosambi. Slight vignette acceptable to draw eye to centre. Crop to exact 4:5.

---

### GENERATION_PROMPTS

**Final execution prompt:**

*A 4:5 vertical premium product photograph of a tall glass containing pale golden sparkling mosambi (sweet lime) water, carbonation bubbles clearly visible, positioned in the upper-centre portion of the frame. One fresh, whole mosambi fruit, matte-skinned, green-yellow, sits in sharp focus to the lower left of the glass base, slightly overlapped by the glass edge. Background is cool white or soft grey, seamless and empty. Soft diffused daylight from above illuminates the glass rim and liquid clarity. The fruit is naturally lit with no shiny oil. No text, no garnish, no ice, no secondary objects. Minimal negative space. Photography style: editorial, refined, contemporary. Colour grading: warm gold for the liquid, true greens and yellows for the fruit. Sharp, clean, modern. High-end beverage advertising aesthetic, not mass-market.*

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Mosambi fruit reference image(s):** Source one or two clear photographs of fresh mosambi from a library or supplier to ensure the model understands the fruit's exact appearance (colour, skin texture, size relative to the glass).
- **Glass reference:** Provide an image of the target glassware (tall, refined, minimalist—e.g., a simple tumbler or highball-style glass) to anchor the generation.
- **Colour reference:** Supply a swatch or sample image of the target liquid colour (pale golden amber) to guide hue.

These references act as visual briefs; they do not become part of the final image.

---

### AUDIO_AND_EDIT

Not applicable. This is a still image for social and mobile display.

---

### FAILURE_PREVENTION

**Failure modes and guardrails:**

1. **Overdesigned/cluttered image:** If the generation adds garnish, secondary fruit, condensation droplets, or a busy background, regenerate with explicit instruction: "Minimal. Nothing but the glass, the drink, and one mosambi fruit. Empty background. No clutter."

2. **Artificial or neon liquid colour:** If the liquid appears too bright, over-saturated, or fluorescent, request: "The sparkling water should be pale warm gold, natural-looking, not artificially bright. Like fresh pressed mosambi juice, not candy."

3. **Mosambi unrecognisable:** If the fruit looks generic or wrong, supply the reference image and request: "The fruit is a mosambi—pale yellow-green, round, thin skin, citrus. Match the provided reference image exactly."

4. **Text or branding creep:** If the model adds a product label, text, or brand mark, explicitly state: "No text. No labels. No branding visible. Image only."

5. **Wrong aspect ratio:** Ensure the final crop is exactly 4:5 (vertical, 1000 × 1250 pixels for digital use, or to client spec).

6. **Cheap or generic aesthetic:** If the image reads as a mass-market soft drink ad (gaudy, plastic, lifestyle-heavy), regenerate with: "Premium, editorial aesthetic. Refined simplicity. This is a contemporary craft beverage, not a mass-market product. Minimalist composition. Think luxury sparkling water or premium juice, not cola."

7. **Wrong lighting:** If shadows are harsh or the glass looks opaque, request: "Soft, diffused light. The glass and liquid must be crystal clear and luminous. Show the carbonation. Rim light on the glassware to emphasise premium quality."

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 vertical  
✅ **Product as hero:** Drink glass is the unmistakable focal point  
✅ **Mosambi included:** Fruit present and recognisable  
✅ **No clichéd "Indian" visual shorthand:** No flags, patterns, Taj Mahal, peacocks, or decorative geometry  
✅ **Sophisticated, not cheap:** Minimal, editorial, refined aesthetic; premium glassware; clean light  
✅ **Refreshing & contemporary:** Cool light, visible carbonation, modern composition  
✅ **Culturally familiar yet contemporary:** Mosambi is recognisable to the target audience and grounds the product in Indian citrus tradition; the execution is globally contemporary  
✅ **No celebrity:** None present  
✅ **No external website:** No links, QR codes, or URLs  
✅ **No text overlay:** Image is self-sufficient  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Canon sources used:**

1. **Ogilvy on Advertising, Ch. 2: "Make the Product the Hero"** (ACCEPTED)  
   - Application: Centring the glass and mosambi fruit as the unmistakable hero; rejecting decorative or lifestyle-heavy framing.

2. **Samara, *Making and Breaking the Grid*, Ch. 1: "Negative Space as Shape"** (ACCEPTED)  
   - Application: Treating empty space (white/grey background) as a compositional element of equal importance; breathing room in a 4:5 vertical format.

3. **Dwyer & Patel, *Cinema India*, Ch. 4: "Cultural Construction of Meaning" and related Q&A** (ACCEPTED)  
   - Application: Understanding that cultural specificity (mosambi) need not rely on text or ornamental shorthand; authentic presence of the ingredient itself communicates identity. Avoiding cliché by trusting the object's own meaning rather than layering decorative "Indian-ness."

**External websites:** None consulted or required.

---

**Ready for creative execution.**

## CORE_CREATIVE_IDEA
**The Conversation Between Fruit and Refinement**

A single tall sparkling drink glass, half-filled with bright pale-amber liquid and visible carbonation, sits in neutral/cool light. One fresh mosambi fruit—cut or whole, unblemished, jewel-like—is positioned adjacent or slightly behind the glass, in sharp focus. Minimal negative space. No garnish clutter. The composition reveals:
- The drink's genuine colour and clarity (not artificial sweetness)
- The recognisable mosambi fruit as proof of ingredient authenticity
- Modern glassware suggesting premium positioning
- Restraint and craft, not volume or excess

The image reads as "sophisticated everyday" rather than "luxury spectacle" or "mass-market party."

---

### MESSAGE_AND_INFORMATION_HIERARCHY
1. **Primary:** The drink (glass, colour, carbonation) as the hero and trust signal
2. **Secondary:** The mosambi fruit as the cultural/ingredient anchor and proof of identity
3. **Tertiary:** Cleanliness, light, contemporary aesthetic (no text needed)

The mosambi does not illustrate the drink; it *validates* it. The drink's appearance sells the experience.

---

### VISUAL_SYSTEM

**Colour palette:**
- Pale warm gold to amber liquid (realistic mosambi sparkling water colour, not over-saturated)
- Cool whites, soft greys, or warm off-whites for background and negative space
- Mosambi: natural greens/yellows, matte and saturated
- No pattern, texture overload, or ornamental geometry

**Lighting:**
- Soft north-light or diffused directional light (no harsh shadows)
- Light enters the glass from above-left to show carbonation bubbles and liquid clarity
- Slight rim light on the glass edge to signal premium glassware
- Mosambi evenly lit, no hard shadows

**Composition:**
- Vertical 4:5 format: glass occupies the upper two-thirds (liquid filling roughly the middle zone), mosambi positioned lower-left or lower-right, slightly overlapping the glass base or sitting independently below
- Breathing room: 15–20% of frame is negative space (white or neutral)
- No clutter; no ice, no straw, no secondary objects

**Typography:**
- None in the image itself

---

### PRODUCTION_RECIPE

1. **Set dressing:** Clean white or pale grey seamless background (paper or painted wall). Minimal reflector fill; key light from above at 45°, soft diffusion.

2. **Glassware:** Tall, refined glass (straight or very slightly tapered). No branding visible. Fill with prepared mosambi sparkling water (or craft a visually identical mixture: pale golden sparkling water + mosambi juice or food colouring to exact the right tone). Ensure carbonation is visible; shoot soon after preparation.

3. **Fruit:** One fresh mosambi, unblemished. Shoot it whole and in-focus adjacent to the glass. Optional: one cross-section showing interior, placed nearby. Keep skin natural; do not over-oil or polish.

4. **Camera position:** Slightly above tabletop height (15–20° angle down); centred on the glass, mosambi in secondary focus zone.

5. **Post-production:** Minimal retouching. Correct exposure and colour balance to ensure the liquid reads as fresh and natural, not artificial or oversaturated. Sharpen the fruit. Leave natural skin texture on the mosambi. Slight vignette acceptable to draw eye to centre. Crop to exact 4:5.

---

### GENERATION_PROMPTS

**Final execution prompt:**

*A 4:5 vertical premium product photograph of a tall glass containing pale golden sparkling mosambi (sweet lime) water, carbonation bubbles clearly visible, positioned in the upper-centre portion of the frame. One fresh, whole mosambi fruit, matte-skinned, green-yellow, sits in sharp focus to the lower left of the glass base, slightly overlapped by the glass edge. Background is cool white or soft grey, seamless and empty. Soft diffused daylight from above illuminates the glass rim and liquid clarity. The fruit is naturally lit with no shiny oil. No text, no garnish, no ice, no secondary objects. Minimal negative space. Photography style: editorial, refined, contemporary. Colour grading: warm gold for the liquid, true greens and yellows for the fruit. Sharp, clean, modern. High-end beverage advertising aesthetic, not mass-market.*

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Mosambi fruit reference image(s):** Source one or two clear photographs of fresh mosambi from a library or supplier to ensure the model understands the fruit's exact appearance (colour, skin texture, size relative to the glass).
- **Glass reference:** Provide an image of the target glassware (tall, refined, minimalist—e.g., a simple tumbler or highball-style glass) to anchor the generation.
- **Colour reference:** Supply a swatch or sample image of the target liquid colour (pale golden amber) to guide hue.

These references act as visual briefs; they do not become part of the final image.

---

### AUDIO_AND_EDIT

Not applicable. This is a still image for social and mobile display.

---

### FAILURE_PREVENTION

**Failure modes and guardrails:**

1. **Overdesigned/cluttered image:** If the generation adds garnish, secondary fruit, condensation droplets, or a busy background, regenerate with explicit instruction: "Minimal. Nothing but the glass, the drink, and one mosambi fruit. Empty background. No clutter."

2. **Artificial or neon liquid colour:** If the liquid appears too bright, over-saturated, or fluorescent, request: "The sparkling water should be pale warm gold, natural-looking, not artificially bright. Like fresh pressed mosambi juice, not candy."

3. **Mosambi unrecognisable:** If the fruit looks generic or wrong, supply the reference image and request: "The fruit is a mosambi—pale yellow-green, round, thin skin, citrus. Match the provided reference image exactly."

4. **Text or branding creep:** If the model adds a product label, text, or brand mark, explicitly state: "No text. No labels. No branding visible. Image only."

5. **Wrong aspect ratio:** Ensure the final crop is exactly 4:5 (vertical, 1000 × 1250 pixels for digital use, or to client spec).

6. **Cheap or generic aesthetic:** If the image reads as a mass-market soft drink ad (gaudy, plastic, lifestyle-heavy), regenerate with: "Premium, editorial aesthetic. Refined simplicity. This is a contemporary craft beverage, not a mass-market product. Minimalist composition. Think luxury sparkling water or premium juice, not cola."

7. **Wrong lighting:** If shadows are harsh or the glass looks opaque, request: "Soft, diffused light. The glass and liquid must be crystal clear and luminous. Show the carbonation. Rim light on the glassware to emphasise premium quality."

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 vertical  
✅ **Product as hero:** Drink glass is the unmistakable focal point  
✅ **Mosambi included:** Fruit present and recognisable  
✅ **No clichéd "Indian" visual shorthand:** No flags, patterns, Taj Mahal, peacocks, or decorative geometry  
✅ **Sophisticated, not cheap:** Minimal, editorial, refined aesthetic; premium glassware; clean light  
✅ **Refreshing & contemporary:** Cool light, visible carbonation, modern composition  
✅ **Culturally familiar yet contemporary:** Mosambi is recognisable to the target audience and grounds the product in Indian citrus tradition; the execution is globally contemporary  
✅ **No celebrity:** None present  
✅ **No external website:** No links, QR codes, or URLs  
✅ **No text overlay:** Image is self-sufficient  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Canon sources used:**

1. **Ogilvy on Advertising, Ch. 2: "Make the Product the Hero"** (ACCEPTED)  
   - Application: Centring the glass and mosambi fruit as the unmistakable hero; rejecting decorative or lifestyle-heavy framing.

2. **Samara, *Making and Breaking the Grid*, Ch. 1: "Negative Space as Shape"** (ACCEPTED)  
   - Application: Treating empty space (white/grey background) as a compositional element of equal importance; breathing room in a 4:5 vertical format.

3. **Dwyer & Patel, *Cinema India*, Ch. 4: "Cultural Construction of Meaning" and related Q&A** (ACCEPTED)  
   - Application: Understanding that cultural specificity (mosambi) need not rely on text or ornamental shorthand; authentic presence of the ingredient itself communicates identity. Avoiding cliché by trusting the object's own meaning rather than layering decorative "Indian-ness."

**External websites:** None consulted or required.

---

**Ready for creative execution.**

## MESSAGE_AND_INFORMATION_HIERARCHY
1. **Primary:** The drink (glass, colour, carbonation) as the hero and trust signal
2. **Secondary:** The mosambi fruit as the cultural/ingredient anchor and proof of identity
3. **Tertiary:** Cleanliness, light, contemporary aesthetic (no text needed)

The mosambi does not illustrate the drink; it *validates* it. The drink's appearance sells the experience.

---

### VISUAL_SYSTEM

**Colour palette:**
- Pale warm gold to amber liquid (realistic mosambi sparkling water colour, not over-saturated)
- Cool whites, soft greys, or warm off-whites for background and negative space
- Mosambi: natural greens/yellows, matte and saturated
- No pattern, texture overload, or ornamental geometry

**Lighting:**
- Soft north-light or diffused directional light (no harsh shadows)
- Light enters the glass from above-left to show carbonation bubbles and liquid clarity
- Slight rim light on the glass edge to signal premium glassware
- Mosambi evenly lit, no hard shadows

**Composition:**
- Vertical 4:5 format: glass occupies the upper two-thirds (liquid filling roughly the middle zone), mosambi positioned lower-left or lower-right, slightly overlapping the glass base or sitting independently below
- Breathing room: 15–20% of frame is negative space (white or neutral)
- No clutter; no ice, no straw, no secondary objects

**Typography:**
- None in the image itself

---

### PRODUCTION_RECIPE

1. **Set dressing:** Clean white or pale grey seamless background (paper or painted wall). Minimal reflector fill; key light from above at 45°, soft diffusion.

2. **Glassware:** Tall, refined glass (straight or very slightly tapered). No branding visible. Fill with prepared mosambi sparkling water (or craft a visually identical mixture: pale golden sparkling water + mosambi juice or food colouring to exact the right tone). Ensure carbonation is visible; shoot soon after preparation.

3. **Fruit:** One fresh mosambi, unblemished. Shoot it whole and in-focus adjacent to the glass. Optional: one cross-section showing interior, placed nearby. Keep skin natural; do not over-oil or polish.

4. **Camera position:** Slightly above tabletop height (15–20° angle down); centred on the glass, mosambi in secondary focus zone.

5. **Post-production:** Minimal retouching. Correct exposure and colour balance to ensure the liquid reads as fresh and natural, not artificial or oversaturated. Sharpen the fruit. Leave natural skin texture on the mosambi. Slight vignette acceptable to draw eye to centre. Crop to exact 4:5.

---

### GENERATION_PROMPTS

**Final execution prompt:**

*A 4:5 vertical premium product photograph of a tall glass containing pale golden sparkling mosambi (sweet lime) water, carbonation bubbles clearly visible, positioned in the upper-centre portion of the frame. One fresh, whole mosambi fruit, matte-skinned, green-yellow, sits in sharp focus to the lower left of the glass base, slightly overlapped by the glass edge. Background is cool white or soft grey, seamless and empty. Soft diffused daylight from above illuminates the glass rim and liquid clarity. The fruit is naturally lit with no shiny oil. No text, no garnish, no ice, no secondary objects. Minimal negative space. Photography style: editorial, refined, contemporary. Colour grading: warm gold for the liquid, true greens and yellows for the fruit. Sharp, clean, modern. High-end beverage advertising aesthetic, not mass-market.*

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Mosambi fruit reference image(s):** Source one or two clear photographs of fresh mosambi from a library or supplier to ensure the model understands the fruit's exact appearance (colour, skin texture, size relative to the glass).
- **Glass reference:** Provide an image of the target glassware (tall, refined, minimalist—e.g., a simple tumbler or highball-style glass) to anchor the generation.
- **Colour reference:** Supply a swatch or sample image of the target liquid colour (pale golden amber) to guide hue.

These references act as visual briefs; they do not become part of the final image.

---

### AUDIO_AND_EDIT

Not applicable. This is a still image for social and mobile display.

---

### FAILURE_PREVENTION

**Failure modes and guardrails:**

1. **Overdesigned/cluttered image:** If the generation adds garnish, secondary fruit, condensation droplets, or a busy background, regenerate with explicit instruction: "Minimal. Nothing but the glass, the drink, and one mosambi fruit. Empty background. No clutter."

2. **Artificial or neon liquid colour:** If the liquid appears too bright, over-saturated, or fluorescent, request: "The sparkling water should be pale warm gold, natural-looking, not artificially bright. Like fresh pressed mosambi juice, not candy."

3. **Mosambi unrecognisable:** If the fruit looks generic or wrong, supply the reference image and request: "The fruit is a mosambi—pale yellow-green, round, thin skin, citrus. Match the provided reference image exactly."

4. **Text or branding creep:** If the model adds a product label, text, or brand mark, explicitly state: "No text. No labels. No branding visible. Image only."

5. **Wrong aspect ratio:** Ensure the final crop is exactly 4:5 (vertical, 1000 × 1250 pixels for digital use, or to client spec).

6. **Cheap or generic aesthetic:** If the image reads as a mass-market soft drink ad (gaudy, plastic, lifestyle-heavy), regenerate with: "Premium, editorial aesthetic. Refined simplicity. This is a contemporary craft beverage, not a mass-market product. Minimalist composition. Think luxury sparkling water or premium juice, not cola."

7. **Wrong lighting:** If shadows are harsh or the glass looks opaque, request: "Soft, diffused light. The glass and liquid must be crystal clear and luminous. Show the carbonation. Rim light on the glassware to emphasise premium quality."

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 vertical  
✅ **Product as hero:** Drink glass is the unmistakable focal point  
✅ **Mosambi included:** Fruit present and recognisable  
✅ **No clichéd "Indian" visual shorthand:** No flags, patterns, Taj Mahal, peacocks, or decorative geometry  
✅ **Sophisticated, not cheap:** Minimal, editorial, refined aesthetic; premium glassware; clean light  
✅ **Refreshing & contemporary:** Cool light, visible carbonation, modern composition  
✅ **Culturally familiar yet contemporary:** Mosambi is recognisable to the target audience and grounds the product in Indian citrus tradition; the execution is globally contemporary  
✅ **No celebrity:** None present  
✅ **No external website:** No links, QR codes, or URLs  
✅ **No text overlay:** Image is self-sufficient  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Canon sources used:**

1. **Ogilvy on Advertising, Ch. 2: "Make the Product the Hero"** (ACCEPTED)  
   - Application: Centring the glass and mosambi fruit as the unmistakable hero; rejecting decorative or lifestyle-heavy framing.

2. **Samara, *Making and Breaking the Grid*, Ch. 1: "Negative Space as Shape"** (ACCEPTED)  
   - Application: Treating empty space (white/grey background) as a compositional element of equal importance; breathing room in a 4:5 vertical format.

3. **Dwyer & Patel, *Cinema India*, Ch. 4: "Cultural Construction of Meaning" and related Q&A** (ACCEPTED)  
   - Application: Understanding that cultural specificity (mosambi) need not rely on text or ornamental shorthand; authentic presence of the ingredient itself communicates identity. Avoiding cliché by trusting the object's own meaning rather than layering decorative "Indian-ness."

**External websites:** None consulted or required.

---

**Ready for creative execution.**

## VISUAL_SYSTEM
**Colour palette:**
- Pale warm gold to amber liquid (realistic mosambi sparkling water colour, not over-saturated)
- Cool whites, soft greys, or warm off-whites for background and negative space
- Mosambi: natural greens/yellows, matte and saturated
- No pattern, texture overload, or ornamental geometry

**Lighting:**
- Soft north-light or diffused directional light (no harsh shadows)
- Light enters the glass from above-left to show carbonation bubbles and liquid clarity
- Slight rim light on the glass edge to signal premium glassware
- Mosambi evenly lit, no hard shadows

**Composition:**
- Vertical 4:5 format: glass occupies the upper two-thirds (liquid filling roughly the middle zone), mosambi positioned lower-left or lower-right, slightly overlapping the glass base or sitting independently below
- Breathing room: 15–20% of frame is negative space (white or neutral)
- No clutter; no ice, no straw, no secondary objects

**Typography:**
- None in the image itself

---

### PRODUCTION_RECIPE

1. **Set dressing:** Clean white or pale grey seamless background (paper or painted wall). Minimal reflector fill; key light from above at 45°, soft diffusion.

2. **Glassware:** Tall, refined glass (straight or very slightly tapered). No branding visible. Fill with prepared mosambi sparkling water (or craft a visually identical mixture: pale golden sparkling water + mosambi juice or food colouring to exact the right tone). Ensure carbonation is visible; shoot soon after preparation.

3. **Fruit:** One fresh mosambi, unblemished. Shoot it whole and in-focus adjacent to the glass. Optional: one cross-section showing interior, placed nearby. Keep skin natural; do not over-oil or polish.

4. **Camera position:** Slightly above tabletop height (15–20° angle down); centred on the glass, mosambi in secondary focus zone.

5. **Post-production:** Minimal retouching. Correct exposure and colour balance to ensure the liquid reads as fresh and natural, not artificial or oversaturated. Sharpen the fruit. Leave natural skin texture on the mosambi. Slight vignette acceptable to draw eye to centre. Crop to exact 4:5.

---

### GENERATION_PROMPTS

**Final execution prompt:**

*A 4:5 vertical premium product photograph of a tall glass containing pale golden sparkling mosambi (sweet lime) water, carbonation bubbles clearly visible, positioned in the upper-centre portion of the frame. One fresh, whole mosambi fruit, matte-skinned, green-yellow, sits in sharp focus to the lower left of the glass base, slightly overlapped by the glass edge. Background is cool white or soft grey, seamless and empty. Soft diffused daylight from above illuminates the glass rim and liquid clarity. The fruit is naturally lit with no shiny oil. No text, no garnish, no ice, no secondary objects. Minimal negative space. Photography style: editorial, refined, contemporary. Colour grading: warm gold for the liquid, true greens and yellows for the fruit. Sharp, clean, modern. High-end beverage advertising aesthetic, not mass-market.*

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Mosambi fruit reference image(s):** Source one or two clear photographs of fresh mosambi from a library or supplier to ensure the model understands the fruit's exact appearance (colour, skin texture, size relative to the glass).
- **Glass reference:** Provide an image of the target glassware (tall, refined, minimalist—e.g., a simple tumbler or highball-style glass) to anchor the generation.
- **Colour reference:** Supply a swatch or sample image of the target liquid colour (pale golden amber) to guide hue.

These references act as visual briefs; they do not become part of the final image.

---

### AUDIO_AND_EDIT

Not applicable. This is a still image for social and mobile display.

---

### FAILURE_PREVENTION

**Failure modes and guardrails:**

1. **Overdesigned/cluttered image:** If the generation adds garnish, secondary fruit, condensation droplets, or a busy background, regenerate with explicit instruction: "Minimal. Nothing but the glass, the drink, and one mosambi fruit. Empty background. No clutter."

2. **Artificial or neon liquid colour:** If the liquid appears too bright, over-saturated, or fluorescent, request: "The sparkling water should be pale warm gold, natural-looking, not artificially bright. Like fresh pressed mosambi juice, not candy."

3. **Mosambi unrecognisable:** If the fruit looks generic or wrong, supply the reference image and request: "The fruit is a mosambi—pale yellow-green, round, thin skin, citrus. Match the provided reference image exactly."

4. **Text or branding creep:** If the model adds a product label, text, or brand mark, explicitly state: "No text. No labels. No branding visible. Image only."

5. **Wrong aspect ratio:** Ensure the final crop is exactly 4:5 (vertical, 1000 × 1250 pixels for digital use, or to client spec).

6. **Cheap or generic aesthetic:** If the image reads as a mass-market soft drink ad (gaudy, plastic, lifestyle-heavy), regenerate with: "Premium, editorial aesthetic. Refined simplicity. This is a contemporary craft beverage, not a mass-market product. Minimalist composition. Think luxury sparkling water or premium juice, not cola."

7. **Wrong lighting:** If shadows are harsh or the glass looks opaque, request: "Soft, diffused light. The glass and liquid must be crystal clear and luminous. Show the carbonation. Rim light on the glassware to emphasise premium quality."

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 vertical  
✅ **Product as hero:** Drink glass is the unmistakable focal point  
✅ **Mosambi included:** Fruit present and recognisable  
✅ **No clichéd "Indian" visual shorthand:** No flags, patterns, Taj Mahal, peacocks, or decorative geometry  
✅ **Sophisticated, not cheap:** Minimal, editorial, refined aesthetic; premium glassware; clean light  
✅ **Refreshing & contemporary:** Cool light, visible carbonation, modern composition  
✅ **Culturally familiar yet contemporary:** Mosambi is recognisable to the target audience and grounds the product in Indian citrus tradition; the execution is globally contemporary  
✅ **No celebrity:** None present  
✅ **No external website:** No links, QR codes, or URLs  
✅ **No text overlay:** Image is self-sufficient  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Canon sources used:**

1. **Ogilvy on Advertising, Ch. 2: "Make the Product the Hero"** (ACCEPTED)  
   - Application: Centring the glass and mosambi fruit as the unmistakable hero; rejecting decorative or lifestyle-heavy framing.

2. **Samara, *Making and Breaking the Grid*, Ch. 1: "Negative Space as Shape"** (ACCEPTED)  
   - Application: Treating empty space (white/grey background) as a compositional element of equal importance; breathing room in a 4:5 vertical format.

3. **Dwyer & Patel, *Cinema India*, Ch. 4: "Cultural Construction of Meaning" and related Q&A** (ACCEPTED)  
   - Application: Understanding that cultural specificity (mosambi) need not rely on text or ornamental shorthand; authentic presence of the ingredient itself communicates identity. Avoiding cliché by trusting the object's own meaning rather than layering decorative "Indian-ness."

**External websites:** None consulted or required.

---

**Ready for creative execution.**

## PRODUCTION_RECIPE
1. **Set dressing:** Clean white or pale grey seamless background (paper or painted wall). Minimal reflector fill; key light from above at 45°, soft diffusion.

2. **Glassware:** Tall, refined glass (straight or very slightly tapered). No branding visible. Fill with prepared mosambi sparkling water (or craft a visually identical mixture: pale golden sparkling water + mosambi juice or food colouring to exact the right tone). Ensure carbonation is visible; shoot soon after preparation.

3. **Fruit:** One fresh mosambi, unblemished. Shoot it whole and in-focus adjacent to the glass. Optional: one cross-section showing interior, placed nearby. Keep skin natural; do not over-oil or polish.

4. **Camera position:** Slightly above tabletop height (15–20° angle down); centred on the glass, mosambi in secondary focus zone.

5. **Post-production:** Minimal retouching. Correct exposure and colour balance to ensure the liquid reads as fresh and natural, not artificial or oversaturated. Sharpen the fruit. Leave natural skin texture on the mosambi. Slight vignette acceptable to draw eye to centre. Crop to exact 4:5.

---

### GENERATION_PROMPTS

**Final execution prompt:**

*A 4:5 vertical premium product photograph of a tall glass containing pale golden sparkling mosambi (sweet lime) water, carbonation bubbles clearly visible, positioned in the upper-centre portion of the frame. One fresh, whole mosambi fruit, matte-skinned, green-yellow, sits in sharp focus to the lower left of the glass base, slightly overlapped by the glass edge. Background is cool white or soft grey, seamless and empty. Soft diffused daylight from above illuminates the glass rim and liquid clarity. The fruit is naturally lit with no shiny oil. No text, no garnish, no ice, no secondary objects. Minimal negative space. Photography style: editorial, refined, contemporary. Colour grading: warm gold for the liquid, true greens and yellows for the fruit. Sharp, clean, modern. High-end beverage advertising aesthetic, not mass-market.*

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Mosambi fruit reference image(s):** Source one or two clear photographs of fresh mosambi from a library or supplier to ensure the model understands the fruit's exact appearance (colour, skin texture, size relative to the glass).
- **Glass reference:** Provide an image of the target glassware (tall, refined, minimalist—e.g., a simple tumbler or highball-style glass) to anchor the generation.
- **Colour reference:** Supply a swatch or sample image of the target liquid colour (pale golden amber) to guide hue.

These references act as visual briefs; they do not become part of the final image.

---

### AUDIO_AND_EDIT

Not applicable. This is a still image for social and mobile display.

---

### FAILURE_PREVENTION

**Failure modes and guardrails:**

1. **Overdesigned/cluttered image:** If the generation adds garnish, secondary fruit, condensation droplets, or a busy background, regenerate with explicit instruction: "Minimal. Nothing but the glass, the drink, and one mosambi fruit. Empty background. No clutter."

2. **Artificial or neon liquid colour:** If the liquid appears too bright, over-saturated, or fluorescent, request: "The sparkling water should be pale warm gold, natural-looking, not artificially bright. Like fresh pressed mosambi juice, not candy."

3. **Mosambi unrecognisable:** If the fruit looks generic or wrong, supply the reference image and request: "The fruit is a mosambi—pale yellow-green, round, thin skin, citrus. Match the provided reference image exactly."

4. **Text or branding creep:** If the model adds a product label, text, or brand mark, explicitly state: "No text. No labels. No branding visible. Image only."

5. **Wrong aspect ratio:** Ensure the final crop is exactly 4:5 (vertical, 1000 × 1250 pixels for digital use, or to client spec).

6. **Cheap or generic aesthetic:** If the image reads as a mass-market soft drink ad (gaudy, plastic, lifestyle-heavy), regenerate with: "Premium, editorial aesthetic. Refined simplicity. This is a contemporary craft beverage, not a mass-market product. Minimalist composition. Think luxury sparkling water or premium juice, not cola."

7. **Wrong lighting:** If shadows are harsh or the glass looks opaque, request: "Soft, diffused light. The glass and liquid must be crystal clear and luminous. Show the carbonation. Rim light on the glassware to emphasise premium quality."

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 vertical  
✅ **Product as hero:** Drink glass is the unmistakable focal point  
✅ **Mosambi included:** Fruit present and recognisable  
✅ **No clichéd "Indian" visual shorthand:** No flags, patterns, Taj Mahal, peacocks, or decorative geometry  
✅ **Sophisticated, not cheap:** Minimal, editorial, refined aesthetic; premium glassware; clean light  
✅ **Refreshing & contemporary:** Cool light, visible carbonation, modern composition  
✅ **Culturally familiar yet contemporary:** Mosambi is recognisable to the target audience and grounds the product in Indian citrus tradition; the execution is globally contemporary  
✅ **No celebrity:** None present  
✅ **No external website:** No links, QR codes, or URLs  
✅ **No text overlay:** Image is self-sufficient  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Canon sources used:**

1. **Ogilvy on Advertising, Ch. 2: "Make the Product the Hero"** (ACCEPTED)  
   - Application: Centring the glass and mosambi fruit as the unmistakable hero; rejecting decorative or lifestyle-heavy framing.

2. **Samara, *Making and Breaking the Grid*, Ch. 1: "Negative Space as Shape"** (ACCEPTED)  
   - Application: Treating empty space (white/grey background) as a compositional element of equal importance; breathing room in a 4:5 vertical format.

3. **Dwyer & Patel, *Cinema India*, Ch. 4: "Cultural Construction of Meaning" and related Q&A** (ACCEPTED)  
   - Application: Understanding that cultural specificity (mosambi) need not rely on text or ornamental shorthand; authentic presence of the ingredient itself communicates identity. Avoiding cliché by trusting the object's own meaning rather than layering decorative "Indian-ness."

**External websites:** None consulted or required.

---

**Ready for creative execution.**

## GENERATION_PROMPTS
**Final execution prompt:**

*A 4:5 vertical premium product photograph of a tall glass containing pale golden sparkling mosambi (sweet lime) water, carbonation bubbles clearly visible, positioned in the upper-centre portion of the frame. One fresh, whole mosambi fruit, matte-skinned, green-yellow, sits in sharp focus to the lower left of the glass base, slightly overlapped by the glass edge. Background is cool white or soft grey, seamless and empty. Soft diffused daylight from above illuminates the glass rim and liquid clarity. The fruit is naturally lit with no shiny oil. No text, no garnish, no ice, no secondary objects. Minimal negative space. Photography style: editorial, refined, contemporary. Colour grading: warm gold for the liquid, true greens and yellows for the fruit. Sharp, clean, modern. High-end beverage advertising aesthetic, not mass-market.*

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Mosambi fruit reference image(s):** Source one or two clear photographs of fresh mosambi from a library or supplier to ensure the model understands the fruit's exact appearance (colour, skin texture, size relative to the glass).
- **Glass reference:** Provide an image of the target glassware (tall, refined, minimalist—e.g., a simple tumbler or highball-style glass) to anchor the generation.
- **Colour reference:** Supply a swatch or sample image of the target liquid colour (pale golden amber) to guide hue.

These references act as visual briefs; they do not become part of the final image.

---

### AUDIO_AND_EDIT

Not applicable. This is a still image for social and mobile display.

---

### FAILURE_PREVENTION

**Failure modes and guardrails:**

1. **Overdesigned/cluttered image:** If the generation adds garnish, secondary fruit, condensation droplets, or a busy background, regenerate with explicit instruction: "Minimal. Nothing but the glass, the drink, and one mosambi fruit. Empty background. No clutter."

2. **Artificial or neon liquid colour:** If the liquid appears too bright, over-saturated, or fluorescent, request: "The sparkling water should be pale warm gold, natural-looking, not artificially bright. Like fresh pressed mosambi juice, not candy."

3. **Mosambi unrecognisable:** If the fruit looks generic or wrong, supply the reference image and request: "The fruit is a mosambi—pale yellow-green, round, thin skin, citrus. Match the provided reference image exactly."

4. **Text or branding creep:** If the model adds a product label, text, or brand mark, explicitly state: "No text. No labels. No branding visible. Image only."

5. **Wrong aspect ratio:** Ensure the final crop is exactly 4:5 (vertical, 1000 × 1250 pixels for digital use, or to client spec).

6. **Cheap or generic aesthetic:** If the image reads as a mass-market soft drink ad (gaudy, plastic, lifestyle-heavy), regenerate with: "Premium, editorial aesthetic. Refined simplicity. This is a contemporary craft beverage, not a mass-market product. Minimalist composition. Think luxury sparkling water or premium juice, not cola."

7. **Wrong lighting:** If shadows are harsh or the glass looks opaque, request: "Soft, diffused light. The glass and liquid must be crystal clear and luminous. Show the carbonation. Rim light on the glassware to emphasise premium quality."

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 vertical  
✅ **Product as hero:** Drink glass is the unmistakable focal point  
✅ **Mosambi included:** Fruit present and recognisable  
✅ **No clichéd "Indian" visual shorthand:** No flags, patterns, Taj Mahal, peacocks, or decorative geometry  
✅ **Sophisticated, not cheap:** Minimal, editorial, refined aesthetic; premium glassware; clean light  
✅ **Refreshing & contemporary:** Cool light, visible carbonation, modern composition  
✅ **Culturally familiar yet contemporary:** Mosambi is recognisable to the target audience and grounds the product in Indian citrus tradition; the execution is globally contemporary  
✅ **No celebrity:** None present  
✅ **No external website:** No links, QR codes, or URLs  
✅ **No text overlay:** Image is self-sufficient  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Canon sources used:**

1. **Ogilvy on Advertising, Ch. 2: "Make the Product the Hero"** (ACCEPTED)  
   - Application: Centring the glass and mosambi fruit as the unmistakable hero; rejecting decorative or lifestyle-heavy framing.

2. **Samara, *Making and Breaking the Grid*, Ch. 1: "Negative Space as Shape"** (ACCEPTED)  
   - Application: Treating empty space (white/grey background) as a compositional element of equal importance; breathing room in a 4:5 vertical format.

3. **Dwyer & Patel, *Cinema India*, Ch. 4: "Cultural Construction of Meaning" and related Q&A** (ACCEPTED)  
   - Application: Understanding that cultural specificity (mosambi) need not rely on text or ornamental shorthand; authentic presence of the ingredient itself communicates identity. Avoiding cliché by trusting the object's own meaning rather than layering decorative "Indian-ness."

**External websites:** None consulted or required.

---

**Ready for creative execution.**

## DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS
- **Mosambi fruit reference image(s):** Source one or two clear photographs of fresh mosambi from a library or supplier to ensure the model understands the fruit's exact appearance (colour, skin texture, size relative to the glass).
- **Glass reference:** Provide an image of the target glassware (tall, refined, minimalist—e.g., a simple tumbler or highball-style glass) to anchor the generation.
- **Colour reference:** Supply a swatch or sample image of the target liquid colour (pale golden amber) to guide hue.

These references act as visual briefs; they do not become part of the final image.

---

### AUDIO_AND_EDIT

Not applicable. This is a still image for social and mobile display.

---

### FAILURE_PREVENTION

**Failure modes and guardrails:**

1. **Overdesigned/cluttered image:** If the generation adds garnish, secondary fruit, condensation droplets, or a busy background, regenerate with explicit instruction: "Minimal. Nothing but the glass, the drink, and one mosambi fruit. Empty background. No clutter."

2. **Artificial or neon liquid colour:** If the liquid appears too bright, over-saturated, or fluorescent, request: "The sparkling water should be pale warm gold, natural-looking, not artificially bright. Like fresh pressed mosambi juice, not candy."

3. **Mosambi unrecognisable:** If the fruit looks generic or wrong, supply the reference image and request: "The fruit is a mosambi—pale yellow-green, round, thin skin, citrus. Match the provided reference image exactly."

4. **Text or branding creep:** If the model adds a product label, text, or brand mark, explicitly state: "No text. No labels. No branding visible. Image only."

5. **Wrong aspect ratio:** Ensure the final crop is exactly 4:5 (vertical, 1000 × 1250 pixels for digital use, or to client spec).

6. **Cheap or generic aesthetic:** If the image reads as a mass-market soft drink ad (gaudy, plastic, lifestyle-heavy), regenerate with: "Premium, editorial aesthetic. Refined simplicity. This is a contemporary craft beverage, not a mass-market product. Minimalist composition. Think luxury sparkling water or premium juice, not cola."

7. **Wrong lighting:** If shadows are harsh or the glass looks opaque, request: "Soft, diffused light. The glass and liquid must be crystal clear and luminous. Show the carbonation. Rim light on the glassware to emphasise premium quality."

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 vertical  
✅ **Product as hero:** Drink glass is the unmistakable focal point  
✅ **Mosambi included:** Fruit present and recognisable  
✅ **No clichéd "Indian" visual shorthand:** No flags, patterns, Taj Mahal, peacocks, or decorative geometry  
✅ **Sophisticated, not cheap:** Minimal, editorial, refined aesthetic; premium glassware; clean light  
✅ **Refreshing & contemporary:** Cool light, visible carbonation, modern composition  
✅ **Culturally familiar yet contemporary:** Mosambi is recognisable to the target audience and grounds the product in Indian citrus tradition; the execution is globally contemporary  
✅ **No celebrity:** None present  
✅ **No external website:** No links, QR codes, or URLs  
✅ **No text overlay:** Image is self-sufficient  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Canon sources used:**

1. **Ogilvy on Advertising, Ch. 2: "Make the Product the Hero"** (ACCEPTED)  
   - Application: Centring the glass and mosambi fruit as the unmistakable hero; rejecting decorative or lifestyle-heavy framing.

2. **Samara, *Making and Breaking the Grid*, Ch. 1: "Negative Space as Shape"** (ACCEPTED)  
   - Application: Treating empty space (white/grey background) as a compositional element of equal importance; breathing room in a 4:5 vertical format.

3. **Dwyer & Patel, *Cinema India*, Ch. 4: "Cultural Construction of Meaning" and related Q&A** (ACCEPTED)  
   - Application: Understanding that cultural specificity (mosambi) need not rely on text or ornamental shorthand; authentic presence of the ingredient itself communicates identity. Avoiding cliché by trusting the object's own meaning rather than layering decorative "Indian-ness."

**External websites:** None consulted or required.

---

**Ready for creative execution.**

## FAILURE_PREVENTION
**Failure modes and guardrails:**

1. **Overdesigned/cluttered image:** If the generation adds garnish, secondary fruit, condensation droplets, or a busy background, regenerate with explicit instruction: "Minimal. Nothing but the glass, the drink, and one mosambi fruit. Empty background. No clutter."

2. **Artificial or neon liquid colour:** If the liquid appears too bright, over-saturated, or fluorescent, request: "The sparkling water should be pale warm gold, natural-looking, not artificially bright. Like fresh pressed mosambi juice, not candy."

3. **Mosambi unrecognisable:** If the fruit looks generic or wrong, supply the reference image and request: "The fruit is a mosambi—pale yellow-green, round, thin skin, citrus. Match the provided reference image exactly."

4. **Text or branding creep:** If the model adds a product label, text, or brand mark, explicitly state: "No text. No labels. No branding visible. Image only."

5. **Wrong aspect ratio:** Ensure the final crop is exactly 4:5 (vertical, 1000 × 1250 pixels for digital use, or to client spec).

6. **Cheap or generic aesthetic:** If the image reads as a mass-market soft drink ad (gaudy, plastic, lifestyle-heavy), regenerate with: "Premium, editorial aesthetic. Refined simplicity. This is a contemporary craft beverage, not a mass-market product. Minimalist composition. Think luxury sparkling water or premium juice, not cola."

7. **Wrong lighting:** If shadows are harsh or the glass looks opaque, request: "Soft, diffused light. The glass and liquid must be crystal clear and luminous. Show the carbonation. Rim light on the glassware to emphasise premium quality."

---

### HARD_CONSTRAINT_CHECK

✅ **Format:** 4:5 vertical  
✅ **Product as hero:** Drink glass is the unmistakable focal point  
✅ **Mosambi included:** Fruit present and recognisable  
✅ **No clichéd "Indian" visual shorthand:** No flags, patterns, Taj Mahal, peacocks, or decorative geometry  
✅ **Sophisticated, not cheap:** Minimal, editorial, refined aesthetic; premium glassware; clean light  
✅ **Refreshing & contemporary:** Cool light, visible carbonation, modern composition  
✅ **Culturally familiar yet contemporary:** Mosambi is recognisable to the target audience and grounds the product in Indian citrus tradition; the execution is globally contemporary  
✅ **No celebrity:** None present  
✅ **No external website:** No links, QR codes, or URLs  
✅ **No text overlay:** Image is self-sufficient  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Canon sources used:**

1. **Ogilvy on Advertising, Ch. 2: "Make the Product the Hero"** (ACCEPTED)  
   - Application: Centring the glass and mosambi fruit as the unmistakable hero; rejecting decorative or lifestyle-heavy framing.

2. **Samara, *Making and Breaking the Grid*, Ch. 1: "Negative Space as Shape"** (ACCEPTED)  
   - Application: Treating empty space (white/grey background) as a compositional element of equal importance; breathing room in a 4:5 vertical format.

3. **Dwyer & Patel, *Cinema India*, Ch. 4: "Cultural Construction of Meaning" and related Q&A** (ACCEPTED)  
   - Application: Understanding that cultural specificity (mosambi) need not rely on text or ornamental shorthand; authentic presence of the ingredient itself communicates identity. Avoiding cliché by trusting the object's own meaning rather than layering decorative "Indian-ness."

**External websites:** None consulted or required.

---

**Ready for creative execution.**

## HARD_CONSTRAINT_CHECK
✅ **Format:** 4:5 vertical  
✅ **Product as hero:** Drink glass is the unmistakable focal point  
✅ **Mosambi included:** Fruit present and recognisable  
✅ **No clichéd "Indian" visual shorthand:** No flags, patterns, Taj Mahal, peacocks, or decorative geometry  
✅ **Sophisticated, not cheap:** Minimal, editorial, refined aesthetic; premium glassware; clean light  
✅ **Refreshing & contemporary:** Cool light, visible carbonation, modern composition  
✅ **Culturally familiar yet contemporary:** Mosambi is recognisable to the target audience and grounds the product in Indian citrus tradition; the execution is globally contemporary  
✅ **No celebrity:** None present  
✅ **No external website:** No links, QR codes, or URLs  
✅ **No text overlay:** Image is self-sufficient  

---

### KNOWLEDGE_AND_WEBSITE_USE

**Canon sources used:**

1. **Ogilvy on Advertising, Ch. 2: "Make the Product the Hero"** (ACCEPTED)  
   - Application: Centring the glass and mosambi fruit as the unmistakable hero; rejecting decorative or lifestyle-heavy framing.

2. **Samara, *Making and Breaking the Grid*, Ch. 1: "Negative Space as Shape"** (ACCEPTED)  
   - Application: Treating empty space (white/grey background) as a compositional element of equal importance; breathing room in a 4:5 vertical format.

3. **Dwyer & Patel, *Cinema India*, Ch. 4: "Cultural Construction of Meaning" and related Q&A** (ACCEPTED)  
   - Application: Understanding that cultural specificity (mosambi) need not rely on text or ornamental shorthand; authentic presence of the ingredient itself communicates identity. Avoiding cliché by trusting the object's own meaning rather than layering decorative "Indian-ness."

**External websites:** None consulted or required.

---

**Ready for creative execution.**

## GENERATE I13
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I14 — B03

Source key: E037-haiku-full-canon-B03-R2
Use frozen brief B03 from the top of this file.



## GENERATE I14
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I15 — B03

Source key: E037-haiku-full-canon-B03-R3
Use frozen brief B03 from the top of this file.

## DELIVERABLE
Single 4:5 vertical advertising image. Format: JPG/PNG. Resolution: 1080 × 1350px minimum (Instagram/mobile-first density). Colour-corrected for iOS display, test against warm and daylight monitors.

---

### OBJECTIVE_INTERPRETATION
Produce a premium beverage hero-shot that positions mosambi sparkling water as a contemporary, sophisticated everyday choice for urban adults 22–35. The product must be unmistakably the focal point. Visual strategy should signal "refreshment + refinement + contemporary ease" without deploying recognisable Indian visual clichés (no textiles, mandalas, spice market, gold foil, heritage fonts, temple elements, or saturated colour symbolism). The image must feel like it belongs in a modern urban lifestyle context—minimalist, clean, aspirational—while the mosambi ingredient itself guarantees cultural grounding.

---

### CORE_CREATIVE_IDEA
**Product-as-gateway.** The bottle is the only storyteller. It contains real, recognisable mosambi (visible in the liquid and optionally in a single fresh segment) combined with visible carbonation. The surrounding environment is geometrically composed, neutral in palette, with deliberately negative space to enforce premium positioning. The image reads: "Familiar fruit, unfamiliar sophistication." No narrative, no face, no lifestyle staging—just the object itself and the space it commands.

---

### MESSAGE_AND_INFORMATION_HIERARCHY
1. **Primary:** The product bottle (brand, volume, liquid colour and carbonation)
2. **Secondary:** The presence of real mosambi (visual cue: juice colour, possibly a thin slice or segment as garnish/proof)
3. **Tertiary:** The impression of cleanliness, modernity, and refinement (lighting, space, finish)

No text is necessary. The product *is* the message.

---

### VISUAL_SYSTEM

**Framing and Composition:**
- **Vertical axis:** Product bottle positioned in the upper-middle third, leaving strong negative space below (per Samara: negative space is a shape of equal importance; use this to enforce perceived quality and breathing room)
- **Lighting:** Single, clean light source creating one soft shadow. Avoid harsh multiple shadows. The goal is clarity and polish, not drama
- **Colour palette:** Cool-to-neutral base (soft white, pale grey, or very soft concrete/stone texture). The mosambi inside the bottle should be the only saturated colour element—warm golden-orange juice with visible carbonation bubbles catching light
- **Foreground/support:** A simple prop (minimal—either a thin glass, a single mosambi segment on a neutral surface, or nothing) positioned lower to create visual weight distribution without distraction
- **Depth:** Shallow depth of field acceptable; bottle in sharp focus, background subtly blurred to reinforce that the product is the hero
- **Material language:** Glass clarity, condensation on the bottle (conveys freshness and chill), clean industrial or Scandinavian aesthetic

**Cultural positioning:** The aesthetic is *contemporary minimalism*, not Indian. The mosambi origin is signalled by the fruit itself (unmistakable to Indian consumers, discovered by others), not by typography or décor.

---

### PRODUCTION_RECIPE

1. **Setup:**
   - Simple white or soft grey cyclorama backdrop, or a subtle stone/concrete textured surface (minimal pattern, high contrast control)
   - Single key light at 45° or slightly higher, producing one defined shadow
   - Reflector or fill card opposite the key to control shadow depth (not eliminate it)
   - No background clutter; negative space is intentional

2. **Bottle and content:**
   - Use the actual product bottle if available; if not, a clear glass bottle with custom or near-final label
   - Fill with fresh mosambi juice (golden-orange, vitamin C-rich colour) or a juice-water blend that replicates the final colour
   - Carbonate the liquid in-camera or composite captured bubbles; bubbles should catch and scatter light
   - Optionally include one fresh mosambi segment (thinly sliced) on the surface below, or inside the glass if it's a serving shot
   - Bottle should show condensation or a light mist (spray with distilled water if needed; will evaporate, so plan timing)

3. **Camera and technical:**
   - Shoot at f/2.8–f/5.6 (shallow to moderate depth of field, bottle sharp)
   - Colour temperature: ~5500K (daylight) to lean slightly cool and fresh
   - Avoid high ISO; prioritise lighting over speed
   - Shoot in RAW for post-processing latitude

4. **Post-processing:**
   - Colour: Boost clarity on the mosambi juice and carbonation; keep background soft and neutral
   - Contrast: Lift blacks slightly (premium, not dark and heavy); ensure the bottle silhouette is clean against background
   - Vibrance: Lift the mosambi colour subtly without oversaturating (should feel natural, not candy)
   - Sharpening: Bottle and liquid only; background diffused
   - No vignetting; clean white or grey edges

---

### GENERATION_PROMPTS

**Single final generation prompt (for image synthesis if applicable):**

> A 4:5 vertical product photography shot of a premium sparkling mosambi beverage bottle, centred in the upper-middle frame against a soft white or pale grey background with generous negative space below. The bottle is clear glass, showing vivid golden-orange fresh mosambi juice inside with visible fine carbonation bubbles catching clean directional light from the left. A single fresh mosambi fruit segment rests on a neutral grey surface just below the bottle, slightly to the right. Lighting is soft and singular—one key light at 45°, creating one subtle shadow to the right. The aesthetic is contemporary minimalist, Scandinavian-influenced, clean and refined. High contrast, sharp bottle, soft diffused background. No text, no people, no cultural decorative elements. Photograph, professional studio product shot, high resolution, no grain. Beverage photography, premium brand positioning.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Bottle label:** Deterministic. Use the final approved product label (or a near-final mockup). Do not synthesise the label; composite it in post or use the physical bottle.
- **Mosambi segment (if included):** Fresh fruit, real. Photograph it separately with consistent lighting and composite, or include on set. Colour and texture must be authentic.
- **Liquid colour:** Should match the actual mosambi juice colour (warm golden-orange). If generated, this must be colour-corrected to match reference samples of real mosambi juice.
- **Background surface:** Deterministic. Shoot on actual material (white card, paint, or stone texture) for consistent texture and reflectivity. Do not synthesise.

---

### AUDIO_AND_EDIT
Not applicable for a static image. No audio or animation required.

---

### FAILURE_PREVENTION

**Risk:** The generated image looks like a generic soft-drink advertisement.  
**Mitigation:** Enforce negative space, minimal propping, and cool/neutral palette. Avoid warm backgrounds, tropical elements, or abundance of fruit. The simplicity *is* the premium signal.

**Risk:** The mosambi juice colour appears artificial or too saturated.  
**Mitigation:** Reference real mosambi juice colour cards before generation/post-processing. Mosambi is softer and less acidic-looking than lime or lemon; err toward golden-orange rather than neon.

**Risk:** Carbonation bubbles are too prominent or too subtle.  
**Mitigation:** Ensure bubbles are captured in-camera or composited with proper light refraction. They should be visible and active-looking (freshness cue) but not distracting; aim for a few dozen small bubbles distributed evenly in the liquid.

**Risk:** The image reads as "expensive" rather than "premium contemporary."  
**Mitigation:** Avoid gold, jewel tones, ornate typography, or luxury cues (leather, velvet). Premium = clean, clear, confident simplicity. The mosambi *is* the luxury.

**Risk:** Bottle placement feels off-centre or awkward in 4:5.  
**Mitigation:** Test framing in-camera. Place the bottle cap at roughly 1/4 to 1/3 down from the top; leave 60%+ of the frame below it for negative space. The lower weight makes the format feel intentional and modern, not "small product in a big frame."

---

### HARD_CONSTRAINT_CHECK

✓ **4:5 vertical aspect ratio:** Confirmed.  
✓ **Product is the unmistakable hero:** Yes; framing, lighting, and composition center the bottle and liquid entirely.  
✓ **No clichéd "Indian" visual shorthand:** Yes; aesthetic is minimalist/contemporary, no decorative cultural elements, no heritage colour palette.  
✓ **Sophisticated and refined:** Yes; clean lighting, neutral palette, generous negative space, sharp bottle, premium material language.  
✓ **Refreshing:** Yes; carbonation, condensation, mosambi colour, cool palette.  
✓ **Culturally contemporary:** Yes; minimalism is globally current, mosambi is the cultural signifier (ingredient, not décor).  
✓ **Retains familiarity of mosambi:** Yes; visible fruit inside and/or as garnish; colour unmistakable to Indian consumers.  
✓ **Does not look cheap:** Yes; studio lighting, clean composition, premium materials and finish.  
✓ **No celebrity:** Confirmed, none included.  
✓ **No external website integration:** Confirmed, none required.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources consulted:**
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Make the product the hero" — direct application to bottle-centric framing and the principle that showing the product with simplicity requires courage but delivers credibility.
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Give products an image of quality" — informs the premium aesthetic, clean lighting, and rejection of cheap-looking visual tropes.
- *Freeman, The Photographer's Eye* (ACCEPTED): Framing precedes composition and is about enclosure — used to justify the 4:5 cropping and the decision to leave strong negative space below the bottle.
- *Samara, Making and Breaking the Grid* (ACCEPTED): Negative space as a shape of equal importance — reinforces the use of lower-frame emptiness as a design element that signals premium positioning and visual confidence.
- *Dwyer & Patel, Cinema India* (ACCEPTED): "Text is seen as a cultural barrier" and contrast between text-minimal Indian visual tradition and text-heavy Western advertising — informs the decision to rely on the product image itself rather than text or typography to carry meaning.

No external websites. Recommendations are based on production principles and creative judgment aligned with the knowledge library.

## OBJECTIVE_INTERPRETATION
Produce a premium beverage hero-shot that positions mosambi sparkling water as a contemporary, sophisticated everyday choice for urban adults 22–35. The product must be unmistakably the focal point. Visual strategy should signal "refreshment + refinement + contemporary ease" without deploying recognisable Indian visual clichés (no textiles, mandalas, spice market, gold foil, heritage fonts, temple elements, or saturated colour symbolism). The image must feel like it belongs in a modern urban lifestyle context—minimalist, clean, aspirational—while the mosambi ingredient itself guarantees cultural grounding.

---

### CORE_CREATIVE_IDEA
**Product-as-gateway.** The bottle is the only storyteller. It contains real, recognisable mosambi (visible in the liquid and optionally in a single fresh segment) combined with visible carbonation. The surrounding environment is geometrically composed, neutral in palette, with deliberately negative space to enforce premium positioning. The image reads: "Familiar fruit, unfamiliar sophistication." No narrative, no face, no lifestyle staging—just the object itself and the space it commands.

---

### MESSAGE_AND_INFORMATION_HIERARCHY
1. **Primary:** The product bottle (brand, volume, liquid colour and carbonation)
2. **Secondary:** The presence of real mosambi (visual cue: juice colour, possibly a thin slice or segment as garnish/proof)
3. **Tertiary:** The impression of cleanliness, modernity, and refinement (lighting, space, finish)

No text is necessary. The product *is* the message.

---

### VISUAL_SYSTEM

**Framing and Composition:**
- **Vertical axis:** Product bottle positioned in the upper-middle third, leaving strong negative space below (per Samara: negative space is a shape of equal importance; use this to enforce perceived quality and breathing room)
- **Lighting:** Single, clean light source creating one soft shadow. Avoid harsh multiple shadows. The goal is clarity and polish, not drama
- **Colour palette:** Cool-to-neutral base (soft white, pale grey, or very soft concrete/stone texture). The mosambi inside the bottle should be the only saturated colour element—warm golden-orange juice with visible carbonation bubbles catching light
- **Foreground/support:** A simple prop (minimal—either a thin glass, a single mosambi segment on a neutral surface, or nothing) positioned lower to create visual weight distribution without distraction
- **Depth:** Shallow depth of field acceptable; bottle in sharp focus, background subtly blurred to reinforce that the product is the hero
- **Material language:** Glass clarity, condensation on the bottle (conveys freshness and chill), clean industrial or Scandinavian aesthetic

**Cultural positioning:** The aesthetic is *contemporary minimalism*, not Indian. The mosambi origin is signalled by the fruit itself (unmistakable to Indian consumers, discovered by others), not by typography or décor.

---

### PRODUCTION_RECIPE

1. **Setup:**
   - Simple white or soft grey cyclorama backdrop, or a subtle stone/concrete textured surface (minimal pattern, high contrast control)
   - Single key light at 45° or slightly higher, producing one defined shadow
   - Reflector or fill card opposite the key to control shadow depth (not eliminate it)
   - No background clutter; negative space is intentional

2. **Bottle and content:**
   - Use the actual product bottle if available; if not, a clear glass bottle with custom or near-final label
   - Fill with fresh mosambi juice (golden-orange, vitamin C-rich colour) or a juice-water blend that replicates the final colour
   - Carbonate the liquid in-camera or composite captured bubbles; bubbles should catch and scatter light
   - Optionally include one fresh mosambi segment (thinly sliced) on the surface below, or inside the glass if it's a serving shot
   - Bottle should show condensation or a light mist (spray with distilled water if needed; will evaporate, so plan timing)

3. **Camera and technical:**
   - Shoot at f/2.8–f/5.6 (shallow to moderate depth of field, bottle sharp)
   - Colour temperature: ~5500K (daylight) to lean slightly cool and fresh
   - Avoid high ISO; prioritise lighting over speed
   - Shoot in RAW for post-processing latitude

4. **Post-processing:**
   - Colour: Boost clarity on the mosambi juice and carbonation; keep background soft and neutral
   - Contrast: Lift blacks slightly (premium, not dark and heavy); ensure the bottle silhouette is clean against background
   - Vibrance: Lift the mosambi colour subtly without oversaturating (should feel natural, not candy)
   - Sharpening: Bottle and liquid only; background diffused
   - No vignetting; clean white or grey edges

---

### GENERATION_PROMPTS

**Single final generation prompt (for image synthesis if applicable):**

> A 4:5 vertical product photography shot of a premium sparkling mosambi beverage bottle, centred in the upper-middle frame against a soft white or pale grey background with generous negative space below. The bottle is clear glass, showing vivid golden-orange fresh mosambi juice inside with visible fine carbonation bubbles catching clean directional light from the left. A single fresh mosambi fruit segment rests on a neutral grey surface just below the bottle, slightly to the right. Lighting is soft and singular—one key light at 45°, creating one subtle shadow to the right. The aesthetic is contemporary minimalist, Scandinavian-influenced, clean and refined. High contrast, sharp bottle, soft diffused background. No text, no people, no cultural decorative elements. Photograph, professional studio product shot, high resolution, no grain. Beverage photography, premium brand positioning.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Bottle label:** Deterministic. Use the final approved product label (or a near-final mockup). Do not synthesise the label; composite it in post or use the physical bottle.
- **Mosambi segment (if included):** Fresh fruit, real. Photograph it separately with consistent lighting and composite, or include on set. Colour and texture must be authentic.
- **Liquid colour:** Should match the actual mosambi juice colour (warm golden-orange). If generated, this must be colour-corrected to match reference samples of real mosambi juice.
- **Background surface:** Deterministic. Shoot on actual material (white card, paint, or stone texture) for consistent texture and reflectivity. Do not synthesise.

---

### AUDIO_AND_EDIT
Not applicable for a static image. No audio or animation required.

---

### FAILURE_PREVENTION

**Risk:** The generated image looks like a generic soft-drink advertisement.  
**Mitigation:** Enforce negative space, minimal propping, and cool/neutral palette. Avoid warm backgrounds, tropical elements, or abundance of fruit. The simplicity *is* the premium signal.

**Risk:** The mosambi juice colour appears artificial or too saturated.  
**Mitigation:** Reference real mosambi juice colour cards before generation/post-processing. Mosambi is softer and less acidic-looking than lime or lemon; err toward golden-orange rather than neon.

**Risk:** Carbonation bubbles are too prominent or too subtle.  
**Mitigation:** Ensure bubbles are captured in-camera or composited with proper light refraction. They should be visible and active-looking (freshness cue) but not distracting; aim for a few dozen small bubbles distributed evenly in the liquid.

**Risk:** The image reads as "expensive" rather than "premium contemporary."  
**Mitigation:** Avoid gold, jewel tones, ornate typography, or luxury cues (leather, velvet). Premium = clean, clear, confident simplicity. The mosambi *is* the luxury.

**Risk:** Bottle placement feels off-centre or awkward in 4:5.  
**Mitigation:** Test framing in-camera. Place the bottle cap at roughly 1/4 to 1/3 down from the top; leave 60%+ of the frame below it for negative space. The lower weight makes the format feel intentional and modern, not "small product in a big frame."

---

### HARD_CONSTRAINT_CHECK

✓ **4:5 vertical aspect ratio:** Confirmed.  
✓ **Product is the unmistakable hero:** Yes; framing, lighting, and composition center the bottle and liquid entirely.  
✓ **No clichéd "Indian" visual shorthand:** Yes; aesthetic is minimalist/contemporary, no decorative cultural elements, no heritage colour palette.  
✓ **Sophisticated and refined:** Yes; clean lighting, neutral palette, generous negative space, sharp bottle, premium material language.  
✓ **Refreshing:** Yes; carbonation, condensation, mosambi colour, cool palette.  
✓ **Culturally contemporary:** Yes; minimalism is globally current, mosambi is the cultural signifier (ingredient, not décor).  
✓ **Retains familiarity of mosambi:** Yes; visible fruit inside and/or as garnish; colour unmistakable to Indian consumers.  
✓ **Does not look cheap:** Yes; studio lighting, clean composition, premium materials and finish.  
✓ **No celebrity:** Confirmed, none included.  
✓ **No external website integration:** Confirmed, none required.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources consulted:**
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Make the product the hero" — direct application to bottle-centric framing and the principle that showing the product with simplicity requires courage but delivers credibility.
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Give products an image of quality" — informs the premium aesthetic, clean lighting, and rejection of cheap-looking visual tropes.
- *Freeman, The Photographer's Eye* (ACCEPTED): Framing precedes composition and is about enclosure — used to justify the 4:5 cropping and the decision to leave strong negative space below the bottle.
- *Samara, Making and Breaking the Grid* (ACCEPTED): Negative space as a shape of equal importance — reinforces the use of lower-frame emptiness as a design element that signals premium positioning and visual confidence.
- *Dwyer & Patel, Cinema India* (ACCEPTED): "Text is seen as a cultural barrier" and contrast between text-minimal Indian visual tradition and text-heavy Western advertising — informs the decision to rely on the product image itself rather than text or typography to carry meaning.

No external websites. Recommendations are based on production principles and creative judgment aligned with the knowledge library.

## CORE_CREATIVE_IDEA
**Product-as-gateway.** The bottle is the only storyteller. It contains real, recognisable mosambi (visible in the liquid and optionally in a single fresh segment) combined with visible carbonation. The surrounding environment is geometrically composed, neutral in palette, with deliberately negative space to enforce premium positioning. The image reads: "Familiar fruit, unfamiliar sophistication." No narrative, no face, no lifestyle staging—just the object itself and the space it commands.

---

### MESSAGE_AND_INFORMATION_HIERARCHY
1. **Primary:** The product bottle (brand, volume, liquid colour and carbonation)
2. **Secondary:** The presence of real mosambi (visual cue: juice colour, possibly a thin slice or segment as garnish/proof)
3. **Tertiary:** The impression of cleanliness, modernity, and refinement (lighting, space, finish)

No text is necessary. The product *is* the message.

---

### VISUAL_SYSTEM

**Framing and Composition:**
- **Vertical axis:** Product bottle positioned in the upper-middle third, leaving strong negative space below (per Samara: negative space is a shape of equal importance; use this to enforce perceived quality and breathing room)
- **Lighting:** Single, clean light source creating one soft shadow. Avoid harsh multiple shadows. The goal is clarity and polish, not drama
- **Colour palette:** Cool-to-neutral base (soft white, pale grey, or very soft concrete/stone texture). The mosambi inside the bottle should be the only saturated colour element—warm golden-orange juice with visible carbonation bubbles catching light
- **Foreground/support:** A simple prop (minimal—either a thin glass, a single mosambi segment on a neutral surface, or nothing) positioned lower to create visual weight distribution without distraction
- **Depth:** Shallow depth of field acceptable; bottle in sharp focus, background subtly blurred to reinforce that the product is the hero
- **Material language:** Glass clarity, condensation on the bottle (conveys freshness and chill), clean industrial or Scandinavian aesthetic

**Cultural positioning:** The aesthetic is *contemporary minimalism*, not Indian. The mosambi origin is signalled by the fruit itself (unmistakable to Indian consumers, discovered by others), not by typography or décor.

---

### PRODUCTION_RECIPE

1. **Setup:**
   - Simple white or soft grey cyclorama backdrop, or a subtle stone/concrete textured surface (minimal pattern, high contrast control)
   - Single key light at 45° or slightly higher, producing one defined shadow
   - Reflector or fill card opposite the key to control shadow depth (not eliminate it)
   - No background clutter; negative space is intentional

2. **Bottle and content:**
   - Use the actual product bottle if available; if not, a clear glass bottle with custom or near-final label
   - Fill with fresh mosambi juice (golden-orange, vitamin C-rich colour) or a juice-water blend that replicates the final colour
   - Carbonate the liquid in-camera or composite captured bubbles; bubbles should catch and scatter light
   - Optionally include one fresh mosambi segment (thinly sliced) on the surface below, or inside the glass if it's a serving shot
   - Bottle should show condensation or a light mist (spray with distilled water if needed; will evaporate, so plan timing)

3. **Camera and technical:**
   - Shoot at f/2.8–f/5.6 (shallow to moderate depth of field, bottle sharp)
   - Colour temperature: ~5500K (daylight) to lean slightly cool and fresh
   - Avoid high ISO; prioritise lighting over speed
   - Shoot in RAW for post-processing latitude

4. **Post-processing:**
   - Colour: Boost clarity on the mosambi juice and carbonation; keep background soft and neutral
   - Contrast: Lift blacks slightly (premium, not dark and heavy); ensure the bottle silhouette is clean against background
   - Vibrance: Lift the mosambi colour subtly without oversaturating (should feel natural, not candy)
   - Sharpening: Bottle and liquid only; background diffused
   - No vignetting; clean white or grey edges

---

### GENERATION_PROMPTS

**Single final generation prompt (for image synthesis if applicable):**

> A 4:5 vertical product photography shot of a premium sparkling mosambi beverage bottle, centred in the upper-middle frame against a soft white or pale grey background with generous negative space below. The bottle is clear glass, showing vivid golden-orange fresh mosambi juice inside with visible fine carbonation bubbles catching clean directional light from the left. A single fresh mosambi fruit segment rests on a neutral grey surface just below the bottle, slightly to the right. Lighting is soft and singular—one key light at 45°, creating one subtle shadow to the right. The aesthetic is contemporary minimalist, Scandinavian-influenced, clean and refined. High contrast, sharp bottle, soft diffused background. No text, no people, no cultural decorative elements. Photograph, professional studio product shot, high resolution, no grain. Beverage photography, premium brand positioning.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Bottle label:** Deterministic. Use the final approved product label (or a near-final mockup). Do not synthesise the label; composite it in post or use the physical bottle.
- **Mosambi segment (if included):** Fresh fruit, real. Photograph it separately with consistent lighting and composite, or include on set. Colour and texture must be authentic.
- **Liquid colour:** Should match the actual mosambi juice colour (warm golden-orange). If generated, this must be colour-corrected to match reference samples of real mosambi juice.
- **Background surface:** Deterministic. Shoot on actual material (white card, paint, or stone texture) for consistent texture and reflectivity. Do not synthesise.

---

### AUDIO_AND_EDIT
Not applicable for a static image. No audio or animation required.

---

### FAILURE_PREVENTION

**Risk:** The generated image looks like a generic soft-drink advertisement.  
**Mitigation:** Enforce negative space, minimal propping, and cool/neutral palette. Avoid warm backgrounds, tropical elements, or abundance of fruit. The simplicity *is* the premium signal.

**Risk:** The mosambi juice colour appears artificial or too saturated.  
**Mitigation:** Reference real mosambi juice colour cards before generation/post-processing. Mosambi is softer and less acidic-looking than lime or lemon; err toward golden-orange rather than neon.

**Risk:** Carbonation bubbles are too prominent or too subtle.  
**Mitigation:** Ensure bubbles are captured in-camera or composited with proper light refraction. They should be visible and active-looking (freshness cue) but not distracting; aim for a few dozen small bubbles distributed evenly in the liquid.

**Risk:** The image reads as "expensive" rather than "premium contemporary."  
**Mitigation:** Avoid gold, jewel tones, ornate typography, or luxury cues (leather, velvet). Premium = clean, clear, confident simplicity. The mosambi *is* the luxury.

**Risk:** Bottle placement feels off-centre or awkward in 4:5.  
**Mitigation:** Test framing in-camera. Place the bottle cap at roughly 1/4 to 1/3 down from the top; leave 60%+ of the frame below it for negative space. The lower weight makes the format feel intentional and modern, not "small product in a big frame."

---

### HARD_CONSTRAINT_CHECK

✓ **4:5 vertical aspect ratio:** Confirmed.  
✓ **Product is the unmistakable hero:** Yes; framing, lighting, and composition center the bottle and liquid entirely.  
✓ **No clichéd "Indian" visual shorthand:** Yes; aesthetic is minimalist/contemporary, no decorative cultural elements, no heritage colour palette.  
✓ **Sophisticated and refined:** Yes; clean lighting, neutral palette, generous negative space, sharp bottle, premium material language.  
✓ **Refreshing:** Yes; carbonation, condensation, mosambi colour, cool palette.  
✓ **Culturally contemporary:** Yes; minimalism is globally current, mosambi is the cultural signifier (ingredient, not décor).  
✓ **Retains familiarity of mosambi:** Yes; visible fruit inside and/or as garnish; colour unmistakable to Indian consumers.  
✓ **Does not look cheap:** Yes; studio lighting, clean composition, premium materials and finish.  
✓ **No celebrity:** Confirmed, none included.  
✓ **No external website integration:** Confirmed, none required.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources consulted:**
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Make the product the hero" — direct application to bottle-centric framing and the principle that showing the product with simplicity requires courage but delivers credibility.
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Give products an image of quality" — informs the premium aesthetic, clean lighting, and rejection of cheap-looking visual tropes.
- *Freeman, The Photographer's Eye* (ACCEPTED): Framing precedes composition and is about enclosure — used to justify the 4:5 cropping and the decision to leave strong negative space below the bottle.
- *Samara, Making and Breaking the Grid* (ACCEPTED): Negative space as a shape of equal importance — reinforces the use of lower-frame emptiness as a design element that signals premium positioning and visual confidence.
- *Dwyer & Patel, Cinema India* (ACCEPTED): "Text is seen as a cultural barrier" and contrast between text-minimal Indian visual tradition and text-heavy Western advertising — informs the decision to rely on the product image itself rather than text or typography to carry meaning.

No external websites. Recommendations are based on production principles and creative judgment aligned with the knowledge library.

## MESSAGE_AND_INFORMATION_HIERARCHY
1. **Primary:** The product bottle (brand, volume, liquid colour and carbonation)
2. **Secondary:** The presence of real mosambi (visual cue: juice colour, possibly a thin slice or segment as garnish/proof)
3. **Tertiary:** The impression of cleanliness, modernity, and refinement (lighting, space, finish)

No text is necessary. The product *is* the message.

---

### VISUAL_SYSTEM

**Framing and Composition:**
- **Vertical axis:** Product bottle positioned in the upper-middle third, leaving strong negative space below (per Samara: negative space is a shape of equal importance; use this to enforce perceived quality and breathing room)
- **Lighting:** Single, clean light source creating one soft shadow. Avoid harsh multiple shadows. The goal is clarity and polish, not drama
- **Colour palette:** Cool-to-neutral base (soft white, pale grey, or very soft concrete/stone texture). The mosambi inside the bottle should be the only saturated colour element—warm golden-orange juice with visible carbonation bubbles catching light
- **Foreground/support:** A simple prop (minimal—either a thin glass, a single mosambi segment on a neutral surface, or nothing) positioned lower to create visual weight distribution without distraction
- **Depth:** Shallow depth of field acceptable; bottle in sharp focus, background subtly blurred to reinforce that the product is the hero
- **Material language:** Glass clarity, condensation on the bottle (conveys freshness and chill), clean industrial or Scandinavian aesthetic

**Cultural positioning:** The aesthetic is *contemporary minimalism*, not Indian. The mosambi origin is signalled by the fruit itself (unmistakable to Indian consumers, discovered by others), not by typography or décor.

---

### PRODUCTION_RECIPE

1. **Setup:**
   - Simple white or soft grey cyclorama backdrop, or a subtle stone/concrete textured surface (minimal pattern, high contrast control)
   - Single key light at 45° or slightly higher, producing one defined shadow
   - Reflector or fill card opposite the key to control shadow depth (not eliminate it)
   - No background clutter; negative space is intentional

2. **Bottle and content:**
   - Use the actual product bottle if available; if not, a clear glass bottle with custom or near-final label
   - Fill with fresh mosambi juice (golden-orange, vitamin C-rich colour) or a juice-water blend that replicates the final colour
   - Carbonate the liquid in-camera or composite captured bubbles; bubbles should catch and scatter light
   - Optionally include one fresh mosambi segment (thinly sliced) on the surface below, or inside the glass if it's a serving shot
   - Bottle should show condensation or a light mist (spray with distilled water if needed; will evaporate, so plan timing)

3. **Camera and technical:**
   - Shoot at f/2.8–f/5.6 (shallow to moderate depth of field, bottle sharp)
   - Colour temperature: ~5500K (daylight) to lean slightly cool and fresh
   - Avoid high ISO; prioritise lighting over speed
   - Shoot in RAW for post-processing latitude

4. **Post-processing:**
   - Colour: Boost clarity on the mosambi juice and carbonation; keep background soft and neutral
   - Contrast: Lift blacks slightly (premium, not dark and heavy); ensure the bottle silhouette is clean against background
   - Vibrance: Lift the mosambi colour subtly without oversaturating (should feel natural, not candy)
   - Sharpening: Bottle and liquid only; background diffused
   - No vignetting; clean white or grey edges

---

### GENERATION_PROMPTS

**Single final generation prompt (for image synthesis if applicable):**

> A 4:5 vertical product photography shot of a premium sparkling mosambi beverage bottle, centred in the upper-middle frame against a soft white or pale grey background with generous negative space below. The bottle is clear glass, showing vivid golden-orange fresh mosambi juice inside with visible fine carbonation bubbles catching clean directional light from the left. A single fresh mosambi fruit segment rests on a neutral grey surface just below the bottle, slightly to the right. Lighting is soft and singular—one key light at 45°, creating one subtle shadow to the right. The aesthetic is contemporary minimalist, Scandinavian-influenced, clean and refined. High contrast, sharp bottle, soft diffused background. No text, no people, no cultural decorative elements. Photograph, professional studio product shot, high resolution, no grain. Beverage photography, premium brand positioning.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Bottle label:** Deterministic. Use the final approved product label (or a near-final mockup). Do not synthesise the label; composite it in post or use the physical bottle.
- **Mosambi segment (if included):** Fresh fruit, real. Photograph it separately with consistent lighting and composite, or include on set. Colour and texture must be authentic.
- **Liquid colour:** Should match the actual mosambi juice colour (warm golden-orange). If generated, this must be colour-corrected to match reference samples of real mosambi juice.
- **Background surface:** Deterministic. Shoot on actual material (white card, paint, or stone texture) for consistent texture and reflectivity. Do not synthesise.

---

### AUDIO_AND_EDIT
Not applicable for a static image. No audio or animation required.

---

### FAILURE_PREVENTION

**Risk:** The generated image looks like a generic soft-drink advertisement.  
**Mitigation:** Enforce negative space, minimal propping, and cool/neutral palette. Avoid warm backgrounds, tropical elements, or abundance of fruit. The simplicity *is* the premium signal.

**Risk:** The mosambi juice colour appears artificial or too saturated.  
**Mitigation:** Reference real mosambi juice colour cards before generation/post-processing. Mosambi is softer and less acidic-looking than lime or lemon; err toward golden-orange rather than neon.

**Risk:** Carbonation bubbles are too prominent or too subtle.  
**Mitigation:** Ensure bubbles are captured in-camera or composited with proper light refraction. They should be visible and active-looking (freshness cue) but not distracting; aim for a few dozen small bubbles distributed evenly in the liquid.

**Risk:** The image reads as "expensive" rather than "premium contemporary."  
**Mitigation:** Avoid gold, jewel tones, ornate typography, or luxury cues (leather, velvet). Premium = clean, clear, confident simplicity. The mosambi *is* the luxury.

**Risk:** Bottle placement feels off-centre or awkward in 4:5.  
**Mitigation:** Test framing in-camera. Place the bottle cap at roughly 1/4 to 1/3 down from the top; leave 60%+ of the frame below it for negative space. The lower weight makes the format feel intentional and modern, not "small product in a big frame."

---

### HARD_CONSTRAINT_CHECK

✓ **4:5 vertical aspect ratio:** Confirmed.  
✓ **Product is the unmistakable hero:** Yes; framing, lighting, and composition center the bottle and liquid entirely.  
✓ **No clichéd "Indian" visual shorthand:** Yes; aesthetic is minimalist/contemporary, no decorative cultural elements, no heritage colour palette.  
✓ **Sophisticated and refined:** Yes; clean lighting, neutral palette, generous negative space, sharp bottle, premium material language.  
✓ **Refreshing:** Yes; carbonation, condensation, mosambi colour, cool palette.  
✓ **Culturally contemporary:** Yes; minimalism is globally current, mosambi is the cultural signifier (ingredient, not décor).  
✓ **Retains familiarity of mosambi:** Yes; visible fruit inside and/or as garnish; colour unmistakable to Indian consumers.  
✓ **Does not look cheap:** Yes; studio lighting, clean composition, premium materials and finish.  
✓ **No celebrity:** Confirmed, none included.  
✓ **No external website integration:** Confirmed, none required.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources consulted:**
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Make the product the hero" — direct application to bottle-centric framing and the principle that showing the product with simplicity requires courage but delivers credibility.
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Give products an image of quality" — informs the premium aesthetic, clean lighting, and rejection of cheap-looking visual tropes.
- *Freeman, The Photographer's Eye* (ACCEPTED): Framing precedes composition and is about enclosure — used to justify the 4:5 cropping and the decision to leave strong negative space below the bottle.
- *Samara, Making and Breaking the Grid* (ACCEPTED): Negative space as a shape of equal importance — reinforces the use of lower-frame emptiness as a design element that signals premium positioning and visual confidence.
- *Dwyer & Patel, Cinema India* (ACCEPTED): "Text is seen as a cultural barrier" and contrast between text-minimal Indian visual tradition and text-heavy Western advertising — informs the decision to rely on the product image itself rather than text or typography to carry meaning.

No external websites. Recommendations are based on production principles and creative judgment aligned with the knowledge library.

## VISUAL_SYSTEM
**Framing and Composition:**
- **Vertical axis:** Product bottle positioned in the upper-middle third, leaving strong negative space below (per Samara: negative space is a shape of equal importance; use this to enforce perceived quality and breathing room)
- **Lighting:** Single, clean light source creating one soft shadow. Avoid harsh multiple shadows. The goal is clarity and polish, not drama
- **Colour palette:** Cool-to-neutral base (soft white, pale grey, or very soft concrete/stone texture). The mosambi inside the bottle should be the only saturated colour element—warm golden-orange juice with visible carbonation bubbles catching light
- **Foreground/support:** A simple prop (minimal—either a thin glass, a single mosambi segment on a neutral surface, or nothing) positioned lower to create visual weight distribution without distraction
- **Depth:** Shallow depth of field acceptable; bottle in sharp focus, background subtly blurred to reinforce that the product is the hero
- **Material language:** Glass clarity, condensation on the bottle (conveys freshness and chill), clean industrial or Scandinavian aesthetic

**Cultural positioning:** The aesthetic is *contemporary minimalism*, not Indian. The mosambi origin is signalled by the fruit itself (unmistakable to Indian consumers, discovered by others), not by typography or décor.

---

### PRODUCTION_RECIPE

1. **Setup:**
   - Simple white or soft grey cyclorama backdrop, or a subtle stone/concrete textured surface (minimal pattern, high contrast control)
   - Single key light at 45° or slightly higher, producing one defined shadow
   - Reflector or fill card opposite the key to control shadow depth (not eliminate it)
   - No background clutter; negative space is intentional

2. **Bottle and content:**
   - Use the actual product bottle if available; if not, a clear glass bottle with custom or near-final label
   - Fill with fresh mosambi juice (golden-orange, vitamin C-rich colour) or a juice-water blend that replicates the final colour
   - Carbonate the liquid in-camera or composite captured bubbles; bubbles should catch and scatter light
   - Optionally include one fresh mosambi segment (thinly sliced) on the surface below, or inside the glass if it's a serving shot
   - Bottle should show condensation or a light mist (spray with distilled water if needed; will evaporate, so plan timing)

3. **Camera and technical:**
   - Shoot at f/2.8–f/5.6 (shallow to moderate depth of field, bottle sharp)
   - Colour temperature: ~5500K (daylight) to lean slightly cool and fresh
   - Avoid high ISO; prioritise lighting over speed
   - Shoot in RAW for post-processing latitude

4. **Post-processing:**
   - Colour: Boost clarity on the mosambi juice and carbonation; keep background soft and neutral
   - Contrast: Lift blacks slightly (premium, not dark and heavy); ensure the bottle silhouette is clean against background
   - Vibrance: Lift the mosambi colour subtly without oversaturating (should feel natural, not candy)
   - Sharpening: Bottle and liquid only; background diffused
   - No vignetting; clean white or grey edges

---

### GENERATION_PROMPTS

**Single final generation prompt (for image synthesis if applicable):**

> A 4:5 vertical product photography shot of a premium sparkling mosambi beverage bottle, centred in the upper-middle frame against a soft white or pale grey background with generous negative space below. The bottle is clear glass, showing vivid golden-orange fresh mosambi juice inside with visible fine carbonation bubbles catching clean directional light from the left. A single fresh mosambi fruit segment rests on a neutral grey surface just below the bottle, slightly to the right. Lighting is soft and singular—one key light at 45°, creating one subtle shadow to the right. The aesthetic is contemporary minimalist, Scandinavian-influenced, clean and refined. High contrast, sharp bottle, soft diffused background. No text, no people, no cultural decorative elements. Photograph, professional studio product shot, high resolution, no grain. Beverage photography, premium brand positioning.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Bottle label:** Deterministic. Use the final approved product label (or a near-final mockup). Do not synthesise the label; composite it in post or use the physical bottle.
- **Mosambi segment (if included):** Fresh fruit, real. Photograph it separately with consistent lighting and composite, or include on set. Colour and texture must be authentic.
- **Liquid colour:** Should match the actual mosambi juice colour (warm golden-orange). If generated, this must be colour-corrected to match reference samples of real mosambi juice.
- **Background surface:** Deterministic. Shoot on actual material (white card, paint, or stone texture) for consistent texture and reflectivity. Do not synthesise.

---

### AUDIO_AND_EDIT
Not applicable for a static image. No audio or animation required.

---

### FAILURE_PREVENTION

**Risk:** The generated image looks like a generic soft-drink advertisement.  
**Mitigation:** Enforce negative space, minimal propping, and cool/neutral palette. Avoid warm backgrounds, tropical elements, or abundance of fruit. The simplicity *is* the premium signal.

**Risk:** The mosambi juice colour appears artificial or too saturated.  
**Mitigation:** Reference real mosambi juice colour cards before generation/post-processing. Mosambi is softer and less acidic-looking than lime or lemon; err toward golden-orange rather than neon.

**Risk:** Carbonation bubbles are too prominent or too subtle.  
**Mitigation:** Ensure bubbles are captured in-camera or composited with proper light refraction. They should be visible and active-looking (freshness cue) but not distracting; aim for a few dozen small bubbles distributed evenly in the liquid.

**Risk:** The image reads as "expensive" rather than "premium contemporary."  
**Mitigation:** Avoid gold, jewel tones, ornate typography, or luxury cues (leather, velvet). Premium = clean, clear, confident simplicity. The mosambi *is* the luxury.

**Risk:** Bottle placement feels off-centre or awkward in 4:5.  
**Mitigation:** Test framing in-camera. Place the bottle cap at roughly 1/4 to 1/3 down from the top; leave 60%+ of the frame below it for negative space. The lower weight makes the format feel intentional and modern, not "small product in a big frame."

---

### HARD_CONSTRAINT_CHECK

✓ **4:5 vertical aspect ratio:** Confirmed.  
✓ **Product is the unmistakable hero:** Yes; framing, lighting, and composition center the bottle and liquid entirely.  
✓ **No clichéd "Indian" visual shorthand:** Yes; aesthetic is minimalist/contemporary, no decorative cultural elements, no heritage colour palette.  
✓ **Sophisticated and refined:** Yes; clean lighting, neutral palette, generous negative space, sharp bottle, premium material language.  
✓ **Refreshing:** Yes; carbonation, condensation, mosambi colour, cool palette.  
✓ **Culturally contemporary:** Yes; minimalism is globally current, mosambi is the cultural signifier (ingredient, not décor).  
✓ **Retains familiarity of mosambi:** Yes; visible fruit inside and/or as garnish; colour unmistakable to Indian consumers.  
✓ **Does not look cheap:** Yes; studio lighting, clean composition, premium materials and finish.  
✓ **No celebrity:** Confirmed, none included.  
✓ **No external website integration:** Confirmed, none required.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources consulted:**
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Make the product the hero" — direct application to bottle-centric framing and the principle that showing the product with simplicity requires courage but delivers credibility.
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Give products an image of quality" — informs the premium aesthetic, clean lighting, and rejection of cheap-looking visual tropes.
- *Freeman, The Photographer's Eye* (ACCEPTED): Framing precedes composition and is about enclosure — used to justify the 4:5 cropping and the decision to leave strong negative space below the bottle.
- *Samara, Making and Breaking the Grid* (ACCEPTED): Negative space as a shape of equal importance — reinforces the use of lower-frame emptiness as a design element that signals premium positioning and visual confidence.
- *Dwyer & Patel, Cinema India* (ACCEPTED): "Text is seen as a cultural barrier" and contrast between text-minimal Indian visual tradition and text-heavy Western advertising — informs the decision to rely on the product image itself rather than text or typography to carry meaning.

No external websites. Recommendations are based on production principles and creative judgment aligned with the knowledge library.

## PRODUCTION_RECIPE
1. **Setup:**
   - Simple white or soft grey cyclorama backdrop, or a subtle stone/concrete textured surface (minimal pattern, high contrast control)
   - Single key light at 45° or slightly higher, producing one defined shadow
   - Reflector or fill card opposite the key to control shadow depth (not eliminate it)
   - No background clutter; negative space is intentional

2. **Bottle and content:**
   - Use the actual product bottle if available; if not, a clear glass bottle with custom or near-final label
   - Fill with fresh mosambi juice (golden-orange, vitamin C-rich colour) or a juice-water blend that replicates the final colour
   - Carbonate the liquid in-camera or composite captured bubbles; bubbles should catch and scatter light
   - Optionally include one fresh mosambi segment (thinly sliced) on the surface below, or inside the glass if it's a serving shot
   - Bottle should show condensation or a light mist (spray with distilled water if needed; will evaporate, so plan timing)

3. **Camera and technical:**
   - Shoot at f/2.8–f/5.6 (shallow to moderate depth of field, bottle sharp)
   - Colour temperature: ~5500K (daylight) to lean slightly cool and fresh
   - Avoid high ISO; prioritise lighting over speed
   - Shoot in RAW for post-processing latitude

4. **Post-processing:**
   - Colour: Boost clarity on the mosambi juice and carbonation; keep background soft and neutral
   - Contrast: Lift blacks slightly (premium, not dark and heavy); ensure the bottle silhouette is clean against background
   - Vibrance: Lift the mosambi colour subtly without oversaturating (should feel natural, not candy)
   - Sharpening: Bottle and liquid only; background diffused
   - No vignetting; clean white or grey edges

---

### GENERATION_PROMPTS

**Single final generation prompt (for image synthesis if applicable):**

> A 4:5 vertical product photography shot of a premium sparkling mosambi beverage bottle, centred in the upper-middle frame against a soft white or pale grey background with generous negative space below. The bottle is clear glass, showing vivid golden-orange fresh mosambi juice inside with visible fine carbonation bubbles catching clean directional light from the left. A single fresh mosambi fruit segment rests on a neutral grey surface just below the bottle, slightly to the right. Lighting is soft and singular—one key light at 45°, creating one subtle shadow to the right. The aesthetic is contemporary minimalist, Scandinavian-influenced, clean and refined. High contrast, sharp bottle, soft diffused background. No text, no people, no cultural decorative elements. Photograph, professional studio product shot, high resolution, no grain. Beverage photography, premium brand positioning.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Bottle label:** Deterministic. Use the final approved product label (or a near-final mockup). Do not synthesise the label; composite it in post or use the physical bottle.
- **Mosambi segment (if included):** Fresh fruit, real. Photograph it separately with consistent lighting and composite, or include on set. Colour and texture must be authentic.
- **Liquid colour:** Should match the actual mosambi juice colour (warm golden-orange). If generated, this must be colour-corrected to match reference samples of real mosambi juice.
- **Background surface:** Deterministic. Shoot on actual material (white card, paint, or stone texture) for consistent texture and reflectivity. Do not synthesise.

---

### AUDIO_AND_EDIT
Not applicable for a static image. No audio or animation required.

---

### FAILURE_PREVENTION

**Risk:** The generated image looks like a generic soft-drink advertisement.  
**Mitigation:** Enforce negative space, minimal propping, and cool/neutral palette. Avoid warm backgrounds, tropical elements, or abundance of fruit. The simplicity *is* the premium signal.

**Risk:** The mosambi juice colour appears artificial or too saturated.  
**Mitigation:** Reference real mosambi juice colour cards before generation/post-processing. Mosambi is softer and less acidic-looking than lime or lemon; err toward golden-orange rather than neon.

**Risk:** Carbonation bubbles are too prominent or too subtle.  
**Mitigation:** Ensure bubbles are captured in-camera or composited with proper light refraction. They should be visible and active-looking (freshness cue) but not distracting; aim for a few dozen small bubbles distributed evenly in the liquid.

**Risk:** The image reads as "expensive" rather than "premium contemporary."  
**Mitigation:** Avoid gold, jewel tones, ornate typography, or luxury cues (leather, velvet). Premium = clean, clear, confident simplicity. The mosambi *is* the luxury.

**Risk:** Bottle placement feels off-centre or awkward in 4:5.  
**Mitigation:** Test framing in-camera. Place the bottle cap at roughly 1/4 to 1/3 down from the top; leave 60%+ of the frame below it for negative space. The lower weight makes the format feel intentional and modern, not "small product in a big frame."

---

### HARD_CONSTRAINT_CHECK

✓ **4:5 vertical aspect ratio:** Confirmed.  
✓ **Product is the unmistakable hero:** Yes; framing, lighting, and composition center the bottle and liquid entirely.  
✓ **No clichéd "Indian" visual shorthand:** Yes; aesthetic is minimalist/contemporary, no decorative cultural elements, no heritage colour palette.  
✓ **Sophisticated and refined:** Yes; clean lighting, neutral palette, generous negative space, sharp bottle, premium material language.  
✓ **Refreshing:** Yes; carbonation, condensation, mosambi colour, cool palette.  
✓ **Culturally contemporary:** Yes; minimalism is globally current, mosambi is the cultural signifier (ingredient, not décor).  
✓ **Retains familiarity of mosambi:** Yes; visible fruit inside and/or as garnish; colour unmistakable to Indian consumers.  
✓ **Does not look cheap:** Yes; studio lighting, clean composition, premium materials and finish.  
✓ **No celebrity:** Confirmed, none included.  
✓ **No external website integration:** Confirmed, none required.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources consulted:**
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Make the product the hero" — direct application to bottle-centric framing and the principle that showing the product with simplicity requires courage but delivers credibility.
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Give products an image of quality" — informs the premium aesthetic, clean lighting, and rejection of cheap-looking visual tropes.
- *Freeman, The Photographer's Eye* (ACCEPTED): Framing precedes composition and is about enclosure — used to justify the 4:5 cropping and the decision to leave strong negative space below the bottle.
- *Samara, Making and Breaking the Grid* (ACCEPTED): Negative space as a shape of equal importance — reinforces the use of lower-frame emptiness as a design element that signals premium positioning and visual confidence.
- *Dwyer & Patel, Cinema India* (ACCEPTED): "Text is seen as a cultural barrier" and contrast between text-minimal Indian visual tradition and text-heavy Western advertising — informs the decision to rely on the product image itself rather than text or typography to carry meaning.

No external websites. Recommendations are based on production principles and creative judgment aligned with the knowledge library.

## GENERATION_PROMPTS
**Single final generation prompt (for image synthesis if applicable):**

> A 4:5 vertical product photography shot of a premium sparkling mosambi beverage bottle, centred in the upper-middle frame against a soft white or pale grey background with generous negative space below. The bottle is clear glass, showing vivid golden-orange fresh mosambi juice inside with visible fine carbonation bubbles catching clean directional light from the left. A single fresh mosambi fruit segment rests on a neutral grey surface just below the bottle, slightly to the right. Lighting is soft and singular—one key light at 45°, creating one subtle shadow to the right. The aesthetic is contemporary minimalist, Scandinavian-influenced, clean and refined. High contrast, sharp bottle, soft diffused background. No text, no people, no cultural decorative elements. Photograph, professional studio product shot, high resolution, no grain. Beverage photography, premium brand positioning.

---

### DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS

- **Bottle label:** Deterministic. Use the final approved product label (or a near-final mockup). Do not synthesise the label; composite it in post or use the physical bottle.
- **Mosambi segment (if included):** Fresh fruit, real. Photograph it separately with consistent lighting and composite, or include on set. Colour and texture must be authentic.
- **Liquid colour:** Should match the actual mosambi juice colour (warm golden-orange). If generated, this must be colour-corrected to match reference samples of real mosambi juice.
- **Background surface:** Deterministic. Shoot on actual material (white card, paint, or stone texture) for consistent texture and reflectivity. Do not synthesise.

---

### AUDIO_AND_EDIT
Not applicable for a static image. No audio or animation required.

---

### FAILURE_PREVENTION

**Risk:** The generated image looks like a generic soft-drink advertisement.  
**Mitigation:** Enforce negative space, minimal propping, and cool/neutral palette. Avoid warm backgrounds, tropical elements, or abundance of fruit. The simplicity *is* the premium signal.

**Risk:** The mosambi juice colour appears artificial or too saturated.  
**Mitigation:** Reference real mosambi juice colour cards before generation/post-processing. Mosambi is softer and less acidic-looking than lime or lemon; err toward golden-orange rather than neon.

**Risk:** Carbonation bubbles are too prominent or too subtle.  
**Mitigation:** Ensure bubbles are captured in-camera or composited with proper light refraction. They should be visible and active-looking (freshness cue) but not distracting; aim for a few dozen small bubbles distributed evenly in the liquid.

**Risk:** The image reads as "expensive" rather than "premium contemporary."  
**Mitigation:** Avoid gold, jewel tones, ornate typography, or luxury cues (leather, velvet). Premium = clean, clear, confident simplicity. The mosambi *is* the luxury.

**Risk:** Bottle placement feels off-centre or awkward in 4:5.  
**Mitigation:** Test framing in-camera. Place the bottle cap at roughly 1/4 to 1/3 down from the top; leave 60%+ of the frame below it for negative space. The lower weight makes the format feel intentional and modern, not "small product in a big frame."

---

### HARD_CONSTRAINT_CHECK

✓ **4:5 vertical aspect ratio:** Confirmed.  
✓ **Product is the unmistakable hero:** Yes; framing, lighting, and composition center the bottle and liquid entirely.  
✓ **No clichéd "Indian" visual shorthand:** Yes; aesthetic is minimalist/contemporary, no decorative cultural elements, no heritage colour palette.  
✓ **Sophisticated and refined:** Yes; clean lighting, neutral palette, generous negative space, sharp bottle, premium material language.  
✓ **Refreshing:** Yes; carbonation, condensation, mosambi colour, cool palette.  
✓ **Culturally contemporary:** Yes; minimalism is globally current, mosambi is the cultural signifier (ingredient, not décor).  
✓ **Retains familiarity of mosambi:** Yes; visible fruit inside and/or as garnish; colour unmistakable to Indian consumers.  
✓ **Does not look cheap:** Yes; studio lighting, clean composition, premium materials and finish.  
✓ **No celebrity:** Confirmed, none included.  
✓ **No external website integration:** Confirmed, none required.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources consulted:**
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Make the product the hero" — direct application to bottle-centric framing and the principle that showing the product with simplicity requires courage but delivers credibility.
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Give products an image of quality" — informs the premium aesthetic, clean lighting, and rejection of cheap-looking visual tropes.
- *Freeman, The Photographer's Eye* (ACCEPTED): Framing precedes composition and is about enclosure — used to justify the 4:5 cropping and the decision to leave strong negative space below the bottle.
- *Samara, Making and Breaking the Grid* (ACCEPTED): Negative space as a shape of equal importance — reinforces the use of lower-frame emptiness as a design element that signals premium positioning and visual confidence.
- *Dwyer & Patel, Cinema India* (ACCEPTED): "Text is seen as a cultural barrier" and contrast between text-minimal Indian visual tradition and text-heavy Western advertising — informs the decision to rely on the product image itself rather than text or typography to carry meaning.

No external websites. Recommendations are based on production principles and creative judgment aligned with the knowledge library.

## DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS
- **Bottle label:** Deterministic. Use the final approved product label (or a near-final mockup). Do not synthesise the label; composite it in post or use the physical bottle.
- **Mosambi segment (if included):** Fresh fruit, real. Photograph it separately with consistent lighting and composite, or include on set. Colour and texture must be authentic.
- **Liquid colour:** Should match the actual mosambi juice colour (warm golden-orange). If generated, this must be colour-corrected to match reference samples of real mosambi juice.
- **Background surface:** Deterministic. Shoot on actual material (white card, paint, or stone texture) for consistent texture and reflectivity. Do not synthesise.

---

### AUDIO_AND_EDIT
Not applicable for a static image. No audio or animation required.

---

### FAILURE_PREVENTION

**Risk:** The generated image looks like a generic soft-drink advertisement.  
**Mitigation:** Enforce negative space, minimal propping, and cool/neutral palette. Avoid warm backgrounds, tropical elements, or abundance of fruit. The simplicity *is* the premium signal.

**Risk:** The mosambi juice colour appears artificial or too saturated.  
**Mitigation:** Reference real mosambi juice colour cards before generation/post-processing. Mosambi is softer and less acidic-looking than lime or lemon; err toward golden-orange rather than neon.

**Risk:** Carbonation bubbles are too prominent or too subtle.  
**Mitigation:** Ensure bubbles are captured in-camera or composited with proper light refraction. They should be visible and active-looking (freshness cue) but not distracting; aim for a few dozen small bubbles distributed evenly in the liquid.

**Risk:** The image reads as "expensive" rather than "premium contemporary."  
**Mitigation:** Avoid gold, jewel tones, ornate typography, or luxury cues (leather, velvet). Premium = clean, clear, confident simplicity. The mosambi *is* the luxury.

**Risk:** Bottle placement feels off-centre or awkward in 4:5.  
**Mitigation:** Test framing in-camera. Place the bottle cap at roughly 1/4 to 1/3 down from the top; leave 60%+ of the frame below it for negative space. The lower weight makes the format feel intentional and modern, not "small product in a big frame."

---

### HARD_CONSTRAINT_CHECK

✓ **4:5 vertical aspect ratio:** Confirmed.  
✓ **Product is the unmistakable hero:** Yes; framing, lighting, and composition center the bottle and liquid entirely.  
✓ **No clichéd "Indian" visual shorthand:** Yes; aesthetic is minimalist/contemporary, no decorative cultural elements, no heritage colour palette.  
✓ **Sophisticated and refined:** Yes; clean lighting, neutral palette, generous negative space, sharp bottle, premium material language.  
✓ **Refreshing:** Yes; carbonation, condensation, mosambi colour, cool palette.  
✓ **Culturally contemporary:** Yes; minimalism is globally current, mosambi is the cultural signifier (ingredient, not décor).  
✓ **Retains familiarity of mosambi:** Yes; visible fruit inside and/or as garnish; colour unmistakable to Indian consumers.  
✓ **Does not look cheap:** Yes; studio lighting, clean composition, premium materials and finish.  
✓ **No celebrity:** Confirmed, none included.  
✓ **No external website integration:** Confirmed, none required.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources consulted:**
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Make the product the hero" — direct application to bottle-centric framing and the principle that showing the product with simplicity requires courage but delivers credibility.
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Give products an image of quality" — informs the premium aesthetic, clean lighting, and rejection of cheap-looking visual tropes.
- *Freeman, The Photographer's Eye* (ACCEPTED): Framing precedes composition and is about enclosure — used to justify the 4:5 cropping and the decision to leave strong negative space below the bottle.
- *Samara, Making and Breaking the Grid* (ACCEPTED): Negative space as a shape of equal importance — reinforces the use of lower-frame emptiness as a design element that signals premium positioning and visual confidence.
- *Dwyer & Patel, Cinema India* (ACCEPTED): "Text is seen as a cultural barrier" and contrast between text-minimal Indian visual tradition and text-heavy Western advertising — informs the decision to rely on the product image itself rather than text or typography to carry meaning.

No external websites. Recommendations are based on production principles and creative judgment aligned with the knowledge library.

## FAILURE_PREVENTION
**Risk:** The generated image looks like a generic soft-drink advertisement.  
**Mitigation:** Enforce negative space, minimal propping, and cool/neutral palette. Avoid warm backgrounds, tropical elements, or abundance of fruit. The simplicity *is* the premium signal.

**Risk:** The mosambi juice colour appears artificial or too saturated.  
**Mitigation:** Reference real mosambi juice colour cards before generation/post-processing. Mosambi is softer and less acidic-looking than lime or lemon; err toward golden-orange rather than neon.

**Risk:** Carbonation bubbles are too prominent or too subtle.  
**Mitigation:** Ensure bubbles are captured in-camera or composited with proper light refraction. They should be visible and active-looking (freshness cue) but not distracting; aim for a few dozen small bubbles distributed evenly in the liquid.

**Risk:** The image reads as "expensive" rather than "premium contemporary."  
**Mitigation:** Avoid gold, jewel tones, ornate typography, or luxury cues (leather, velvet). Premium = clean, clear, confident simplicity. The mosambi *is* the luxury.

**Risk:** Bottle placement feels off-centre or awkward in 4:5.  
**Mitigation:** Test framing in-camera. Place the bottle cap at roughly 1/4 to 1/3 down from the top; leave 60%+ of the frame below it for negative space. The lower weight makes the format feel intentional and modern, not "small product in a big frame."

---

### HARD_CONSTRAINT_CHECK

✓ **4:5 vertical aspect ratio:** Confirmed.  
✓ **Product is the unmistakable hero:** Yes; framing, lighting, and composition center the bottle and liquid entirely.  
✓ **No clichéd "Indian" visual shorthand:** Yes; aesthetic is minimalist/contemporary, no decorative cultural elements, no heritage colour palette.  
✓ **Sophisticated and refined:** Yes; clean lighting, neutral palette, generous negative space, sharp bottle, premium material language.  
✓ **Refreshing:** Yes; carbonation, condensation, mosambi colour, cool palette.  
✓ **Culturally contemporary:** Yes; minimalism is globally current, mosambi is the cultural signifier (ingredient, not décor).  
✓ **Retains familiarity of mosambi:** Yes; visible fruit inside and/or as garnish; colour unmistakable to Indian consumers.  
✓ **Does not look cheap:** Yes; studio lighting, clean composition, premium materials and finish.  
✓ **No celebrity:** Confirmed, none included.  
✓ **No external website integration:** Confirmed, none required.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources consulted:**
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Make the product the hero" — direct application to bottle-centric framing and the principle that showing the product with simplicity requires courage but delivers credibility.
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Give products an image of quality" — informs the premium aesthetic, clean lighting, and rejection of cheap-looking visual tropes.
- *Freeman, The Photographer's Eye* (ACCEPTED): Framing precedes composition and is about enclosure — used to justify the 4:5 cropping and the decision to leave strong negative space below the bottle.
- *Samara, Making and Breaking the Grid* (ACCEPTED): Negative space as a shape of equal importance — reinforces the use of lower-frame emptiness as a design element that signals premium positioning and visual confidence.
- *Dwyer & Patel, Cinema India* (ACCEPTED): "Text is seen as a cultural barrier" and contrast between text-minimal Indian visual tradition and text-heavy Western advertising — informs the decision to rely on the product image itself rather than text or typography to carry meaning.

No external websites. Recommendations are based on production principles and creative judgment aligned with the knowledge library.

## HARD_CONSTRAINT_CHECK
✓ **4:5 vertical aspect ratio:** Confirmed.  
✓ **Product is the unmistakable hero:** Yes; framing, lighting, and composition center the bottle and liquid entirely.  
✓ **No clichéd "Indian" visual shorthand:** Yes; aesthetic is minimalist/contemporary, no decorative cultural elements, no heritage colour palette.  
✓ **Sophisticated and refined:** Yes; clean lighting, neutral palette, generous negative space, sharp bottle, premium material language.  
✓ **Refreshing:** Yes; carbonation, condensation, mosambi colour, cool palette.  
✓ **Culturally contemporary:** Yes; minimalism is globally current, mosambi is the cultural signifier (ingredient, not décor).  
✓ **Retains familiarity of mosambi:** Yes; visible fruit inside and/or as garnish; colour unmistakable to Indian consumers.  
✓ **Does not look cheap:** Yes; studio lighting, clean composition, premium materials and finish.  
✓ **No celebrity:** Confirmed, none included.  
✓ **No external website integration:** Confirmed, none required.

---

### KNOWLEDGE_AND_WEBSITE_USE

**Sources consulted:**
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Make the product the hero" — direct application to bottle-centric framing and the principle that showing the product with simplicity requires courage but delivers credibility.
- *Ogilvy on Advertising, Chapter 2* (ACCEPTED): "Give products an image of quality" — informs the premium aesthetic, clean lighting, and rejection of cheap-looking visual tropes.
- *Freeman, The Photographer's Eye* (ACCEPTED): Framing precedes composition and is about enclosure — used to justify the 4:5 cropping and the decision to leave strong negative space below the bottle.
- *Samara, Making and Breaking the Grid* (ACCEPTED): Negative space as a shape of equal importance — reinforces the use of lower-frame emptiness as a design element that signals premium positioning and visual confidence.
- *Dwyer & Patel, Cinema India* (ACCEPTED): "Text is seen as a cultural barrier" and contrast between text-minimal Indian visual tradition and text-heavy Western advertising — informs the decision to rely on the product image itself rather than text or typography to carry meaning.

No external websites. Recommendations are based on production principles and creative judgment aligned with the knowledge library.

## GENERATE I15
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I16 — B06

Source key: E037-haiku-full-canon-B06-R1
Use frozen brief B06 from the top of this file.



## GENERATE I16
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I17 — B06

Source key: E037-haiku-full-canon-B06-R2
Use frozen brief B06 from the top of this file.



## GENERATE I17
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I18 — B06

Source key: E037-haiku-full-canon-B06-R3
Use frozen brief B06 from the top of this file.



## GENERATE I18
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I19 — B02

Source key: E037-sonnet-no-canon-B02-R1
Use frozen brief B02 from the top of this file.



## GENERATE I19
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I20 — B02

Source key: E037-sonnet-no-canon-B02-R2
Use frozen brief B02 from the top of this file.



## GENERATE I20
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I21 — B02

Source key: E037-sonnet-no-canon-B02-R3
Use frozen brief B02 from the top of this file.



## GENERATE I21
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I22 — B03

Source key: E037-sonnet-no-canon-B03-R1
Use frozen brief B03 from the top of this file.



## GENERATE I22
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I23 — B03

Source key: E037-sonnet-no-canon-B03-R2
Use frozen brief B03 from the top of this file.



## GENERATE I23
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I24 — B03

Source key: E037-sonnet-no-canon-B03-R3
Use frozen brief B03 from the top of this file.



## GENERATE I24
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I25 — B06

Source key: E037-sonnet-no-canon-B06-R1
Use frozen brief B06 from the top of this file.



## GENERATE I25
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I26 — B06

Source key: E037-sonnet-no-canon-B06-R2
Use frozen brief B06 from the top of this file.



## GENERATE I26
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I27 — B06

Source key: E037-sonnet-no-canon-B06-R3
Use frozen brief B06 from the top of this file.



## GENERATE I27
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I28 — B02

Source key: E037SCC-sonnet-B02-R1
Use frozen brief B02 from the top of this file.



## GENERATE I28
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I29 — B02

Source key: E037SCC-sonnet-B02-R2
Use frozen brief B02 from the top of this file.



## GENERATE I29
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I30 — B02

Source key: E037SCC-sonnet-B02-R3
Use frozen brief B02 from the top of this file.



## GENERATE I30
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I31 — B03

Source key: E037SCC-sonnet-B03-R1
Use frozen brief B03 from the top of this file.



## GENERATE I31
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I32 — B03

Source key: E037SCC-sonnet-B03-R2
Use frozen brief B03 from the top of this file.



## GENERATE I32
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I33 — B03

Source key: E037SCC-sonnet-B03-R3
Use frozen brief B03 from the top of this file.



## GENERATE I33
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I34 — B06

Source key: E037SCC-sonnet-B06-R1
Use frozen brief B06 from the top of this file.



## GENERATE I34
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I35 — B06

Source key: E037SCC-sonnet-B06-R2
Use frozen brief B06 from the top of this file.



## GENERATE I35
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I36 — B06

Source key: E037SCC-sonnet-B06-R3
Use frozen brief B06 from the top of this file.



## GENERATE I36
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I37 — B02

Source key: E037-gemma-no-canon-B02-R1
Use frozen brief B02 from the top of this file.



## GENERATE I37
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I38 — B02

Source key: E037-gemma-no-canon-B02-R2
Use frozen brief B02 from the top of this file.



## GENERATE I38
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I39 — B02

Source key: E037-gemma-no-canon-B02-R3
Use frozen brief B02 from the top of this file.



## GENERATE I39
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I40 — B03

Source key: E037-gemma-no-canon-B03-R1
Use frozen brief B03 from the top of this file.



## GENERATE I40
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I41 — B03

Source key: E037-gemma-no-canon-B03-R2
Use frozen brief B03 from the top of this file.



## GENERATE I41
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I42 — B03

Source key: E037-gemma-no-canon-B03-R3
Use frozen brief B03 from the top of this file.



## GENERATE I42
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I43 — B06

Source key: E037-gemma-no-canon-B06-R1
Use frozen brief B06 from the top of this file.



## GENERATE I43
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I44 — B06

Source key: E037-gemma-no-canon-B06-R2
Use frozen brief B06 from the top of this file.



## GENERATE I44
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I45 — B06

Source key: E037-gemma-no-canon-B06-R3
Use frozen brief B06 from the top of this file.



## GENERATE I45
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I46 — B02

Source key: E037-gemma-full-canon-B02-R1
Use frozen brief B02 from the top of this file.



## GENERATE I46
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I47 — B02

Source key: E037-gemma-full-canon-B02-R2
Use frozen brief B02 from the top of this file.



## GENERATE I47
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I48 — B02

Source key: E037-gemma-full-canon-B02-R3
Use frozen brief B02 from the top of this file.



## GENERATE I48
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I49 — B03

Source key: E037-gemma-full-canon-B03-R1
Use frozen brief B03 from the top of this file.



## GENERATE I49
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I50 — B03

Source key: E037-gemma-full-canon-B03-R2
Use frozen brief B03 from the top of this file.



## GENERATE I50
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I51 — B03

Source key: E037-gemma-full-canon-B03-R3
Use frozen brief B03 from the top of this file.



## GENERATE I51
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I52 — B06

Source key: E037-gemma-full-canon-B06-R1
Use frozen brief B06 from the top of this file.



## GENERATE I52
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I53 — B06

Source key: E037-gemma-full-canon-B06-R2
Use frozen brief B06 from the top of this file.



## GENERATE I53
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I54 — B06

Source key: E037-gemma-full-canon-B06-R3
Use frozen brief B06 from the top of this file.



## GENERATE I54
Generate one first-pass image. Persist/checkpoint before continuing. Use the bounded-repair rule only for an objective hard failure.

---

# IMAGE JOB I55 — B02

Source key: E037-sonnet-full-canon-B02-R2
Use frozen brief B02 from the top of this file.



## GENERATE I55
Generate one first-pass image. Persist/checkpoint. Use the bounded-repair rule only for an objective hard failure.

---

# END OF IMAGE INPUT

Expected total: **55 image jobs**.
