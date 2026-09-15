#!/usr/bin/env python3
"""Portfolio production, tiles 4 (IronLeaf) and 6 (GyaanBox). Credits route for the clip per Vaibhav (15 Sep). Ledger: v4/gen/LEDGER.jsonl."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import gen4 as G
V4 = G.V3
IRONLEAF = ("Clean premium ecommerce packshot of a fictional plant-protein supplement: one matte forest-green cylindrical tub with a brushed "
            "steel screw lid and a single small embossed leaf symbol centred on the tub, NO LETTERS, NO WORDS, NO NUMBERS, NO READABLE LABEL "
            "TEXT anywhere. Upright, fully visible, no cropping, three-quarter view. Warm off-white seamless studio background, soft diffused "
            "daylight from upper left, realistic product photography, subtle contact shadow, premium DTC supplement aesthetic. No hands, no "
            "people, no scoop, no powder, no extra props, no duplicate tub.")
GYAAN = ("Vertical 9:16 textless plate for an education ad: a bright modern study desk by a window, an open notebook, a pen, a mug of chai, "
         "a small potted plant, soft morning daylight from the left, shallow depth, warm neutral palette, generous clean negative space in the "
         "upper half for later typography. ABSOLUTELY NO TEXT: no writing in the notebook, no labels, no screens, no posters, no logos. No people, no hands.")
what = sys.argv[1]
if what == "ironleaf":
    body = {"prompt": IRONLEAF, "image_size": {"width": 1024, "height": 1280}, "quality": "medium", "num_images": 1, "output_format": "png", "background": "opaque"}
    G.fal("pf-ironleaf-packshot-r1", "openai/gpt-image-2", body, 1, V4 / "gen/portfolio/ironleaf-packshot-r1.png", IRONLEAF, "portfolio tile 4 packshot (fal, USD 0.053 of 0.26)")
elif what == "gyaan-plate":
    G.nb2("pf-gyaan-plate-r1", GYAAN, V4 / "gen/portfolio/gyaan-plate-r1.png", "9:16", "portfolio tile 6 textless plate (credits)")
elif what == "gyaan-motion":
    prompt = ("Animate only this still: very slow push-in, sunlight drifting gently across the desk, steam rising from the mug, the plant's leaves "
              "barely moving. No people, no hands, no new objects, no writing appears, no letters, no logos, no camera shake, no morphing.")
    G.omni_i2v("pf-gyaan-motion-r1", prompt, V4 / "gen/portfolio/gyaan-plate-accepted.png", V4 / "gen/portfolio/gyaan-motion-r1.mp4", 10, "720p", "9:16")
