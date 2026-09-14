#!/usr/bin/env python3
"""Still-image dispatches for V3 (prompts verbatim from the Controller package). One draw each; judged by a human before
any dependent call. usage: stills.py <slot> [--fallback]   slots: a0 kora brewa0 a1 a2 a3 b1 b2 b3 dhaba"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import gen as G  # noqa: E402

V3 = G.V3
OUT = V3 / "gen"
P = {
 "a0": ("Clean premium ecommerce packshot of a fictional skincare serum product: one 30 ml frosted amber-glass dropper bottle, matte ivory rubber bulb and ivory collar, one small abstract copper sun symbol centred on the bottle, NO LETTERS, NO WORDS, NO NUMBERS, NO READABLE LABEL TEXT anywhere on the product. Upright, fully visible, no cropping. Warm off-white seamless studio background. Soft diffused daylight from upper left, believable glass reflections, realistic product photography, subtle contact shadow, high-end Indian/global DTC skincare aesthetic. No hands, no people, no extra props, no duplicate bottle.", (1024, 1280)),
 "kora": ("Premium contemporary Indian fashion campaign still for a fictional womenswear brand. Rich oxblood and saffron silk textiles arranged as an elegant flowing garment study in a modern architectural set, sculptural fabric movement, beautiful controlled shadow, high-fashion editorial lighting, no visible brand logo, no readable text, no signage, no watermark. Human presence only if needed as an anonymous cropped silhouette with no identifiable face. Strong negative space for later ad copy. Sophisticated, not wedding-catalogue, not gaudy.", (1536, 864)),
 "brewa0": ("Clean ecommerce packshot of a fictional premium electric kettle. Matte deep-sage cylindrical kettle body, brushed stainless narrow spout, distinct walnut wood handle and small walnut lid knob, black circular base, NO WORDS, NO LETTERS, NO LOGOS, NO NUMBERS anywhere. Three-quarter view, fully visible, physically plausible proportions, warm-white seamless background, soft commercial studio lighting, crisp edges, no cropping, no hands, no additional appliances.", (1024, 1280)),
 "a1": ("Preserve the supplied bottle EXACTLY: geometry, ivory dropper, amber glass, copper sun mark and proportions. Place it upright on a pale travertine plinth beside a thin reflecting-water surface at warm early-morning light. One large soft light source from camera-left. Refined coral/amber reflections, tiny believable condensation only, premium skincare campaign photography. Large clean negative space upper-left for later typography. No letters, words, price tags, logos, signs or additional labels. No hands. Do not crop the product.", (1920, 1080), "a0"),
 "a2": ("Preserve the supplied bottle exactly. Place it on a minimal warm-stone bathroom vanity beside a folded ivory hand towel and one small ceramic dish. Soft window daylight, quiet premium morning routine, slight depth of field, clean negative space on right for later typography. No additional bottles. No people, no hands, no readable text, no labels, no signage. Bottle remains fully visible and unchanged.", (1280, 1600), "a0"),
 "a3": ("Preserve the supplied bottle exactly. Place it on a dark burgundy stone plinth with restrained marigold petals and one small warm diya well behind the product, elegant contemporary Indian festive visual, not wedding decor, not cluttered. Controlled warm key light and subtle rim light. Negative space upper-left. No readable text, no added label, no hands or people. Bottle geometry and colours unchanged.", (1920, 1080), "a0"),
 "b1": ("Preserve the supplied kettle exactly. Place on a minimal pale-oak kitchen counter in a contemporary sunlit kitchen, ceramic cup nearby, gentle morning steam in background, kettle fully visible, no people, no text, no logo.", (1920, 1080), "brewa0"),
 "b2": ("Preserve the supplied kettle exactly. Place on a small breakfast table by a large window, linen napkin, cup and simple toast plate, cool early morning city light, elegant realistic lifestyle photograph, no people, no text.", (1920, 1080), "brewa0"),
 "b3": ("Preserve the supplied kettle exactly. Place on a sophisticated dark-stone counter with warm evening light and restrained festive greenery, premium DTC campaign visual, no people, no words, no extra appliances.", (1920, 1080), "brewa0"),
 "dhaba": ("Top-down premium commercial photograph of a contemporary Indian restaurant meal on one table: one rich dal bowl, one small jeera rice bowl, two naan, one cucumber-onion salad bowl, one small chutney dish, all fully inside the frame with clean breathing room around every dish, warm appetising natural light, modern dark tabletop, no crop at edges, no people, no packaging, NO LETTERS, NO WORDS, NO MENUS, NO SIGNAGE. Leave clear negative space on upper-left for later offer typography.", (1024, 1280)),
}
ASPECT = {(1024, 1280): "4:5", (1280, 1600): "4:5", (1536, 864): "16:9", (1920, 1080): "16:9"}


def main(slot: str, fallback: bool = False, suffix: str = "r1", ref_override: str | None = None):
    entry = P[slot]; prompt, size = entry[0], entry[1]
    ref = entry[2] if len(entry) > 2 else None
    if ref:  # Seedream 5 Pro Edit with the accepted packshot as the supplied product reference
        ref_path = Path(ref_override) if ref_override else (OUT / "stills" / f"{ref}-accepted.png")
        body = {"prompt": prompt, "image_urls": [G.C.data_uri(ref_path)], "num_images": 1,
                "image_size": {"width": size[0], "height": size[1]}, "output_format": "png"}
        out = OUT / "stills" / f"{slot}-{suffix}.png"
        return G.fal(f"{slot}-{suffix}", "bytedance/seedream/v5/pro/edit", body, 1, out, prompt, f"reference: {ref_path.name}")
    if slot == "dhaba" and not fallback:
        body = {"prompt": prompt, "image_size": {"width": size[0], "height": size[1]}, "output_format": "png", "safety_tolerance": "2"}
        return G.fal(f"{slot}-{suffix}", "fal-ai/flux-2-pro", body, 1, OUT / "stills" / f"{slot}-{suffix}.png", prompt, "text-to-image")
    if fallback:  # Nano Banana 2 (Gemini API credits)
        return G.nb2(f"{slot}-{suffix}-nb2", prompt, OUT / "stills" / f"{slot}-{suffix}-nb2.png", ASPECT[size], "text-to-image fallback")
    body = {"prompt": prompt, "image_size": {"width": size[0], "height": size[1]}, "quality": "medium", "num_images": 1, "output_format": "png", "background": "opaque"}
    return G.fal(f"{slot}-{suffix}", "openai/gpt-image-2", body, 1, OUT / "stills" / f"{slot}-{suffix}.png", prompt, "text-to-image")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], "--fallback" in a, next((x.split("=")[1] for x in a if x.startswith("--suffix=")), "r1"),
         next((x.split("=")[1] for x in a if x.startswith("--ref=")), None))
