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
