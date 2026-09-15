import sys; sys.path.insert(0, 'v4/tools'); import gen4 as G, yaml
PF = yaml.safe_load(open('v4/plan/COPY-PF.yaml'))['nivaas']
which = sys.argv[1]
if which == "ext":
    prompt = ("Animate only this still. Very slow, steady upward camera drift and gentle push-in on the building at dusk; the garden lights glow; "
              f"leaves move slightly. A calm female Indian English narrator says, off screen, exactly: \"{PF['vo_line_1']}\" Quiet evening ambience under the voice, "
              "no music. No people, no cars, no new objects. NO TEXT appears anywhere: no signs, no logos, no captions, no subtitles. No camera shake, no morphing.")
    G.veo_i2v("pf-nivaas2-ext-motion-r1", prompt, G.V3 / "gen/portfolio/nivaas2-ext-accepted.png", G.V3 / "gen/portfolio/nivaas2-ext-motion-r1.mp4", 8, "1080p", True, "9:16")
else:
    prompt = ("Animate only this still. Very slow lateral camera glide across the living room toward the balcony; soft daylight shifts on the wall; the plant "
              f"leaves barely move. The same calm female Indian English narrator says, off screen, exactly: \"{PF['vo_line_2']}\" Quiet room tone under the voice, "
              "no music. No people, no new objects. NO TEXT appears anywhere: no screens, no signs, no logos, no captions, no subtitles. No camera shake, no morphing.")
    G.veo_i2v("pf-nivaas2-int-motion-r1", prompt, G.V3 / "gen/portfolio/nivaas2-int-accepted.png", G.V3 / "gen/portfolio/nivaas2-int-motion-r1.mp4", 8, "1080p", True, "9:16")
