#!/usr/bin/env python3
"""v5 build + assembly: one presenter chain (three pieces), five benefit groups, one caption rule.
usage: build_v2.py <out_dir>
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import adcomp as A  # noqa: E402
import film as F  # noqa: E402
import film2 as F2  # noqa: E402
from assemble import sfx  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
GEN = HERE / "gen"
REPO = HERE.parents[1]
PROJ = Path.home() / "Vaibhav_Personal_Projects"
LIB = REPO / "eval/experiments/EVAL-040/runs"
D = F.DECK
MEDIA = {
    "plate": GEN / "a0-plate/a0-r1.png",
    "biryani_plate": LIB / "img-r1/artifacts/media/IMG-CORE-03__nano-banana-2__core__r2.png",
    "sweets_static": LIB / "img-r1-composite/artifacts/media/IMG-TEXT-01__flux-2-pro__C_composite_textless_base__r1.composite-v2.png",
    "aarohi_motion": GEN / "overlays/aarohi-motion.mp4",
    "sweets_motion": LIB / "topo3-video/artifacts/media/VID-TOPO3-01__minimax-h3-max-i2v__C_textless_plate_i2v_composite__r1.composite.mp4",
    "juice": GEN / "overlays/juice-offer.mp4",
    "chai": PROJ / "aight-website/assets/gallery/videos/aight_chai-composite.mp4",
    "watch": REPO / "eval/experiments/EVAL-038/media/E038-media-B06-haiku-packs.jpg",
    "mumbai": PROJ / "aight-website/assets/gallery/images/seedream_mumbai.png",
    "chain": GEN / "p2-presenter-chain/chain-final.mp4",
    "chain_times": GEN / "p2-presenter-chain/chain-final-times.json",
    "music": LIB / "aud-music-lyria/artifacts/media/MUS-02__lyria__native__r1.wav",
}


def main(out_dir: str):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    seg = out / "seg"; seg.mkdir(exist_ok=True)
    plate = Image.open(MEDIA["plate"]).convert("RGBA")
    en = D["aarohi_en"]
    copy_en = A.Copy("en", en["headline"], en["pill"], en["product"], en["price"], en["was"], en["code"], en["cta"], en["legal"])
    brand = A.Brand(wordmark=en["wordmark"])
    for s in [*en["headline"], en["pill"], en["product"], en["price"], en["was"], en["code"], en["cta"], en["legal"], en["wordmark"]]:
        F.USED_STRINGS.add(s)
    dh = D["dhaba_hi"]
    copy_dh = A.Copy("hi", dh["headline"], dh["pill"], dh["product"], dh["price"], dh["was"], dh["code"], dh["cta"], dh["legal"])
    brand_dh = A.Brand(primary="#7A1F1F", accent="#E4B33C", cream="#F4EFE6", wordmark=dh["wordmark"])
    for s in [*dh["headline"], dh["pill"], dh["product"], dh["price"], dh["was"], dh["code"], dh["cta"], dh["legal"], dh["wordmark"]]:
        F.USED_STRINGS.add(s)
    T, L = D["benefit_tabs"], D["labels"]
    for s in list(T.values()) + list(L.values()): F.USED_STRINGS.add(s)

    order = []  # (name, path, dur, sfx list relative)
    def add(name, path, dur, snaps=()):
        order.append((name, path, dur, list(snaps)))

    # --- presenter chain pieces (captions from transcript timings)
    tm = json.loads(MEDIA["chain_times"].read_text())
    S = D["supers"]; pad = 0.15
    c_open = [(tm[0]["start_s"], tm[0]["end_s"] + pad, S["s1"]), (tm[1]["start_s"], tm[1]["end_s"] + pad, S["s2"]), (tm[2]["start_s"], min(8.0, tm[2]["end_s"] + 0.4), S["s3"])]
    # insert: the finished ad while sentence 1 is spoken
    ad = A.ledge(plate, copy_en, brand, "4x5"); f = F.ground(); card = F.shadowed(F.fit_h(ad, int(F.H * 0.78)))
    A.paste(f, card, int(F.W * 0.70) - card.width // 2, (F.H - card.height) // 2); f.convert("RGB").save(out / "insert-ad.png")
    d_open = F.burn_supers(MEDIA["chain"], seg / "p-open.mp4", c_open, insert=(str(out / "insert-ad.png"), tm[0]["end_s"]), trim_s=8.0)
    c_mid = [(tm[3]["start_s"] - 8.0, tm[3]["end_s"] - 8.0 + pad, S["s4"]), (tm[4]["start_s"] - 8.0, min(7.0, tm[4]["end_s"] - 8.0 + 0.5), S["s5"])]
    d_mid = F.burn_supers(MEDIA["chain"], seg / "p-mid.mp4", c_mid, start_s=8.0, trim_s=7.0)
    c_close = [(tm[5]["start_s"] - 15.0, tm[5]["end_s"] - 15.0 + pad, S["s6"], S["s6_qualifier"]), (tm[6]["start_s"] - 15.0, 7.04, S["s7"])]
    d_close = F.burn_supers(MEDIA["chain"], seg / "p-close.mp4", c_close, start_s=15.0)

    add("open", seg / "p-open.mp4", d_open, [(0.0, "snap", 0.35)])
    # --- G1 finished statics
    n = F.seg_brief(plate, seg / "brief.mp4", 2.0); add("brief", seg / "brief.mp4", n / F.FPS)
    n, snaps = F2.seg_build(plate, copy_en, brand, seg / "build.mp4", 3.3, T["g1"], L["build"], 0.3); add("build", seg / "build.mp4", n / F.FPS, [(s, "snap", 0.5) for s in snaps])
    n = F2.seg_sizes(plate, copy_en, brand, seg / "sizes.mp4", 2.5, T["g1"], L["sizes"]); add("sizes", seg / "sizes.mp4", n / F.FPS, [(0.1, "snap", 0.5)])
    bir = A.ledge(Image.open(MEDIA["biryani_plate"]).convert("RGBA"), copy_dh, brand_dh, "4x5"); bir.convert("RGB").save(out / "biryani-ad.png")
    n = F2.seg_still(bir, seg / "biryani.mp4", 2.5, T["g1"], L["biryani"]); add("biryani", seg / "biryani.mp4", n / F.FPS, [(0.05, "snap", 0.4)])
    # --- G2 angles + Hindi
    n, flip = F2.seg_hooks(plate, brand, seg / "hooks.mp4", 3.5, T["g2"], L["hooks"], 0.2); add("hooks", seg / "hooks.mp4", n / F.FPS, [(0.15 * j + 0.1, "snap", 0.35) for j in range(6)] + [(flip, "tone", 0.6)])
    sw = Image.open(MEDIA["sweets_static"]).convert("RGBA")
    n = F2.seg_still(sw, seg / "sweets-static.mp4", 2.0, T["g2"], L["sweets_static"]); add("sweets_static", seg / "sweets-static.mp4", n / F.FPS, [(0.05, "snap", 0.4)])
    # --- G3 the check
    n, fix = F2.seg_check(brand, seg / "check.mp4", 3.0, T["g3"], L["check"], 0.2); add("check", seg / "check.mp4", n / F.FPS, [(fix, "tick", 0.7)])
    # --- G4 video ads
    F2.seg_clip_card(MEDIA["aarohi_motion"], seg / "aarohi-motion.mp4", 0.2, 2.8, T["g4"], L["aarohi_motion"], aspect=9 / 16); add("aarohi_motion", seg / "aarohi-motion.mp4", 2.8, [(0.0, "snap", 0.35)])
    F2.seg_clip_card(MEDIA["sweets_motion"], seg / "sweets-motion.mp4", 0.5, 2.4, T["g4"], L["sweets_motion"], aspect=9 / 16); add("sweets_motion", seg / "sweets-motion.mp4", 2.4, [(0.0, "snap", 0.35)])
    F2.seg_clip_card(MEDIA["juice"], seg / "juice.mp4", 0.6, 2.4, T["g4"], L["juice"], aspect=9 / 16); add("juice", seg / "juice.mp4", 2.4, [(0.0, "snap", 0.35)])
    # --- G5 range
    F2.seg_clip_card(MEDIA["chai"], seg / "chai.mp4", 0.6, 2.6, T["g5"], L["chai"], aspect=16 / 9, h_frac=0.66); add("chai", seg / "chai.mp4", 2.6, [(0.0, "snap", 0.35)])
    n = F2.seg_still(Image.open(MEDIA["watch"]).convert("RGBA"), seg / "watch.mp4", 1.9, T["g5"], L["watch"]); add("watch", seg / "watch.mp4", n / F.FPS, [(0.05, "snap", 0.4)])
    n = F2.seg_still(Image.open(MEDIA["mumbai"]).convert("RGBA"), seg / "mumbai.mp4", 1.9, T["g5"], L["mumbai"], h_frac=0.66); add("mumbai", seg / "mumbai.mp4", n / F.FPS, [(0.05, "snap", 0.4)])
    # --- presenter mid + close, end card
    add("mid", seg / "p-mid.mp4", d_mid); add("close", seg / "p-close.mp4", d_close)
    n = F.seg_endcard(seg / "end.mp4", 4.3); add("end", seg / "end.mp4", n / F.FPS)

    bad = F.d3_check()
    starts = {}; t = 0.0
    for name, path, dur, _ in order: starts[name] = t; t += dur
    total = t
    lst = out / "concat.txt"; lst.write_text("".join(f"file '{p.resolve()}'\n" for _, p, _, _ in order))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "24", str(out / "video.mp4")], check=True)

    # --- audio: chain pieces at offsets, bed, sfx, loudness
    sfxd = out / "sfx"; sfxd.mkdir(exist_ok=True)
    for k in ("snap", "tone", "tick"): sfx(sfxd / f"{k}.wav", k)
    events = []
    for name, _, _, ev in order:
        events += [(starts[name] + e[0], e[1], e[2]) for e in ev]
    speech = [("open", seg / "p-open.mp4"), ("mid", seg / "p-mid.mp4"), ("close", seg / "p-close.mp4")]
    inputs = ["-i", str(out / "video.mp4")] + sum([["-i", str(p)] for _, p in speech], []) + ["-i", str(MEDIA["music"])] + sum([["-i", str(sfxd / f"{e[1]}.wav")] for e in events], [])
    fc = []
    for k, (name, _) in enumerate(speech, start=1):
        ms = int(starts[name] * 1000)
        fc.append(f"[{k}:a]loudnorm=I=-18:TP=-2:LRA=9,adelay={ms}|{ms}[sp{k}]")
    m_in = starts["brief"]; m_end = total - 0.5
    duck = [(starts["mid"], starts["end"])]
    vol = "*".join(f"if(between(t,{a:.2f},{b:.2f}),0.28,1.0)" for a, b in duck)
    fc.append("[4:a]asplit[m0][m1];[m0][m1]acrossfade=d=3:c1=tri:c2=tri[ml]")
    fc.append(f"[ml]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume='{vol}':eval=frame,afade=t=in:st={m_in:.2f}:d=1.5,afade=t=out:st={m_end-2.5:.2f}:d=2.0,volume=0.16,adelay={int(m_in*1000)}|{int(m_in*1000)},atrim=0:{total:.3f}[mus]")
    labels = []
    for i, e in enumerate(events):
        ms = int(e[0] * 1000); fc.append(f"[{5+i}:a]volume={e[2]},adelay={ms}|{ms},aformat=channel_layouts=stereo[s{i}]"); labels.append(f"[s{i}]")
    fc.append(f"[sp1][sp2][sp3][mus]{''.join(labels)}amix=inputs={4+len(events)}:normalize=0:duration=longest,atrim=0:{total:.3f}[aout]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[aout]", "-c:a", "pcm_s16le", "-ar", "48000", str(out / "mix.wav")], check=True)
    meas = subprocess.run(["ffmpeg", "-i", str(out / "mix.wav"), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    cur = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    ln = f"volume={-16.0 - cur:.2f}dB,alimiter=limit=0.87:attack=5:release=60:level=false"
    final = out / "upwork-intro-v2.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(out / "video.mp4"), "-i", str(out / "mix.wav"), "-af", ln, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{total:.3f}", str(final)], check=True)
    (out / "timeline.json").write_text(json.dumps({"starts": starts, "total_s": total, "events": events, "d3_off_deck": bad}, indent=1, ensure_ascii=False))
    print(json.dumps({"total_s": round(total, 2), "starts": {k: round(v, 2) for k, v in starts.items()}, "d3_off_deck": bad}, indent=0, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
