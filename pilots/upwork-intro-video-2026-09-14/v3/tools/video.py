#!/usr/bin/env python3
"""Image-to-video dispatches (prompts verbatim from the Controller package). Kling v3 Pro primary (silent), Wan 3.0 Prime
fallback, H3 Max second fallback for a non-critical interior only. usage: video.py <slot> <seconds> [--wan|--h3] [--suffix=r1]"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import gen as G

V3 = G.V3
P = {
 "a1": "Animate only the accepted still. Preserve bottle shape, amber colour, ivory dropper, copper sun mark and proportions exactly. Slow controlled dolly-in with a subtle clockwise orbit. Tiny water ripple and slight natural shift in sunlight. Product remains upright and dominant. No hands. No new objects. No letters, words, symbols or labels appear. No sudden zoom, no camera shake, no morphing.",
 "a2": "Animate only the accepted vanity still. Preserve the bottle exactly. Very slow lateral camera drift and subtle focus transition toward the product; gentle daylight changes on the wall. Towel may move imperceptibly. No people, no hands, no new products, no added lettering, no label changes, no geometry changes.",
 "a3": "Animate only the accepted festive still. Preserve the bottle exactly. Slow elegant push-in. Very subtle diya flicker and one or two marigold petals move slightly from natural air. No new objects, no smoke covering product, no letters/text, no changes to bottle or cap.",
 "b1": "Preserve the supplied kettle exactly. Quiet camera and environmental movement only: very slow push-in, soft steam drifting, gentle daylight shift. No product morphing, no people, no hands, no new objects, no letters or text.",
 "b2": "Preserve the supplied kettle exactly. Quiet camera and environmental movement only: slow lateral drift, cool morning light shifting slightly through the window. No product morphing, no people, no new objects, no letters or text.",
 "b3": "Preserve the supplied kettle exactly. Quiet camera and environmental movement only: slow elegant push-in, warm evening light, restrained movement in the greenery. No product morphing, no people, no new objects, no letters or text.",
 "kora": "Preserve scene and garment design. Slow editorial camera glide, restrained fabric movement as if from a gentle studio fan, elegant moving highlights. No new person, no face, no lettering, no logos, no wardrobe transformation.",
}
NEG = "blur, distort, low quality, text, letters, watermark, logo, hands, people, morphing, camera shake"

if __name__ == "__main__":
    slot, secs = sys.argv[1], int(sys.argv[2]); a = sys.argv[3:]
    suffix = next((x.split("=")[1] for x in a if x.startswith("--suffix=")), "r1")
    still = V3 / "gen/stills" / f"{slot}-accepted.png"
    src = f"reference still: {still.name}"
    if "--wan" in a:
        body = {"prompt": P[slot], "start_image_url": G.C.data_uri(still), "resolution": "720p", "duration": secs, "audio": False,
                "aspect_ratio": "16:9" if slot != "a2" else "3:4", "enable_prompt_expansion": True}
        G.fal(f"vid-{slot}-{suffix}-wan", "alibaba/wan-3.0-prime/image-to-video", body, secs, V3 / "gen/video" / f"{slot}-{suffix}-wan.mp4", P[slot], src, "fallback route")
    elif "--h3" in a:
        body = {"prompt": P[slot], "prompt_expansion_mode": "balanced", "image_url": G.C.data_uri(still), "resolution": "768P", "duration": secs}
        G.fal(f"vid-{slot}-{suffix}-h3", "minimax/h3-max/image-to-video", body, secs, V3 / "gen/video" / f"{slot}-{suffix}-h3.mp4", P[slot], src, "second fallback (non-critical)")
    else:
        body = {"prompt": P[slot], "start_image_url": G.C.data_uri(still), "duration": str(secs), "generate_audio": False, "negative_prompt": NEG, "cfg_scale": 0.5}
        G.fal(f"vid-{slot}-{suffix}", "fal-ai/kling-video/v3/pro/image-to-video", body, secs, V3 / "gen/video" / f"{slot}-{suffix}.mp4", P[slot], src, "primary route")
