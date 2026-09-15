import sys; sys.path.insert(0, 'v4/tools'); import gen4 as G, yaml
from pathlib import Path
PF = yaml.safe_load(open('v4/plan/COPY-PF.yaml'))['nivaas']
P1 = ("Vertical 9:16 real-estate film shot, photoreal: slow rising drone-style move revealing a modern mid-rise residential apartment building "
      "in Bengaluru at golden hour, glass balconies, landscaped garden, a few trees, warm evening light. A calm female Indian English narrator "
      f"says clearly, off screen: \"{PF['vo_line_1']}\" Natural ambience under the voice, no music. NO TEXT anywhere: no signboards, no hoardings, "
      "no logos, no captions, no subtitles. No people close to camera.")
P2 = ("Continue: cut to the interior of a bright model apartment — a living room with large windows, soft daylight, a modern sofa, plants, a "
      f"balcony view of trees; slow lateral camera glide. The same calm female Indian English narrator says: \"{PF['vo_line_2']}\" "
      "No music. NO TEXT anywhere: no signs, no screens, no captions, no logos. No people.")
G.veo_t2v_extend("pf-nivaas-story-r1", P1, P2, G.V3 / "gen/portfolio/nivaas-story-r1.mp4", "720p", "9:16", True)
