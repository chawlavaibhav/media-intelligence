import sys; sys.path.insert(0, 'v4/tools'); import gen4 as G
from pathlib import Path
EXT = ("Photoreal vertical 9:16 architectural photograph for a fictional Bengaluru residential project: a modern mid-rise apartment building, "
       "twelve floors, glass-railed balconies, warm stone and off-white facade, mature trees and a landscaped lawn in the foreground, golden-hour "
       "side light, clear evening sky, slight low-angle view from the garden path. Premium real-estate campaign quality, sharp, natural colours. "
       "ABSOLUTELY NO TEXT: no signboards, hoardings, logos, numbers or lettering anywhere. No people, no cars.")
INT = ("Photoreal vertical 9:16 interior photograph of a bright model apartment living room in the same project: floor-to-ceiling windows with a "
       "balcony and treetops beyond, soft daylight, a modern linen sofa, an oak coffee table, a large indoor plant, warm neutral palette, subtle "
       "depth, generous clean space in the upper third. Premium real-estate campaign quality, sharp. ABSOLUTELY NO TEXT: no screens, no books "
       "with titles, no art with lettering, no logos. No people.")
which = sys.argv[1]
body = {"prompt": EXT if which == "ext" else INT, "image_size": {"width": 864, "height": 1536}, "quality": "medium", "num_images": 1, "output_format": "png", "background": "opaque"}
G.fal(f"pf-nivaas2-{which}-r1", "openai/gpt-image-2", body, 1, G.V3 / f"gen/portfolio/nivaas2-{which}-r1.png", body["prompt"], "Nivaas redo: still first (fal)")
