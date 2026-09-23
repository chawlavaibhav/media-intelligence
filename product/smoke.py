"""Deployment smoke test. USD 0: simulated providers and reasoning in a throw-away data directory.

    python3 -m product.smoke            # exit 0 = every stage passed

1. Media engine on THIS host (ffmpeg/ffprobe/rsvg-convert/fonts): compose a still ad with exact text and a
   logo through the compositor gates; build an end card and a super; assemble a film from generated test
   clips + a music bed; run the delivered-file checks (edit lists, loudness/true peak, audio joins).
2. A full dry image job and a dry film job through the real service, orchestrator and worker.
3. Backup and restore of the resulting data directory.
Each step prints PASS/FAIL with the evidence. Nothing here is a quality claim.
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

RESULTS = []


def step(name):
    def wrap(fn):
        try:
            detail = fn()
            RESULTS.append((name, "PASS", detail))
        except Exception as e:  # noqa: BLE001
            RESULTS.append((name, "FAIL", f"{e!r}\n{traceback.format_exc()[-1200:]}"))
        return fn
    return wrap


def media_engine(tmp: Path):
    from product import compose, media, verify
    if not media.have_ffmpeg():
        raise RuntimeError("ffmpeg/ffprobe not installed — the media engine cannot run on this host")
    from PIL import features
    if not features.check("raqm"):
        raise RuntimeError("Pillow has no raqm text shaping on this host — Devanagari would render unshaped (install libraqm0)")
    for probe_text, kind in (("₹2,499", "bold"), ("₹185 प्रति लीटर", "regular")):
        media.measure_text(probe_text, size=48, kind=kind)      # raises if no installed font covers every glyph
    plate = tmp / "plate.png"
    plate.write_bytes(media.sim_image(1080, 1080, seed=3))
    logo = tmp / "logo.svg"
    logo.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="120"><rect width="400" height="120" fill="#1f2a44"/>'
                    '<text x="20" y="80" font-size="64" fill="#fff" font-family="sans-serif">ACME</text></svg>')
    d = {"copy_deck": [{"id": "c1", "text": "Pack less. Go further.", "source": "customer_exact"},
                       {"id": "c2", "text": "₹2,499 · acme.in", "source": "customer_exact"}],
         "composition": {"text_zone": "top"}, "end_card": {"copy_ids": ["c1", "c2"], "background_hex": "#1f2a44"}}
    out, checks, layout = compose.still_ad(plate=plate, out=tmp / "ad.png", aspect="1:1", direction=d, logo=logo, workdir=tmp,
                                           product_box_norm=[0.3, 0.45, 0.7, 0.95])
    bad = [c for c in checks if c["status"] == "FAIL"]
    card, card_checks, _ = compose.end_card(out=tmp / "card.png", size=(1080, 1920), direction=d, logo=logo, workdir=tmp)
    clips = []
    for i in range(3):
        p = tmp / f"clip{i}.mp4"
        p.write_bytes(media.sim_video(4, "9:16", seed=i + 1))
        clips.append(p)
    sup, sup_checks = compose.super_overlay(out=tmp / "super.png", size=(1080, 1920), text="Pack less. Go further.", clip=clips[1],
                                            clip_in=0.0, use=3.5, clip_size=(1080, 1920))
    wav = tmp / "bed.wav"
    from product.providers import _wav
    wav.write_bytes(_wav(20.0))
    rep = media.assemble_film(segments=[{"clip": c, "in": 0.0, "use": 3.5} for c in clips], endcard=card,
                              supers=[{"png": sup, "t_in": 3.7, "t_out": 6.9}], music=wav, out=tmp / "film.mp4", size=(1080, 1920),
                              card_s=3.0, workdir=tmp / "asm")
    p = media.probe(tmp / "film.mp4")
    rows = verify.film_checks(tmp / "film.mp4", cuts=rep["cuts_s"], source_sizes=[[720, 1280]], delivered=(1080, 1920),
                              planned_s=rep["duration_s"], card_in_s=rep["card_in_s"])
    fails = [r for r in rows if r["status"] != "PASS"] + bad + [c for c in card_checks + sup_checks if c["status"] == "FAIL"]
    if fails or abs(p["duration_s"] - rep["duration_s"]) > 0.3 or (p["width"], p["height"]) != (1080, 1920):
        raise RuntimeError(json.dumps({"fails": fails, "probe": p}, default=str)[:1500])
    return {"still_checks": len(checks), "film": p, "film_checks": {r["check_id"]: r["detail"] for r in rows}}


def dry_jobs(tmp: Path):
    from product.tests.support import Env
    e = Env()
    try:
        out = {}
        for media_kind in ("image", "video"):
            jid = e.submit(media_kind)
            e.to_review(jid)
            e.orch.accept(jid, e.user["email"])
            out[media_kind] = {"state": e.state(jid), "attempts": len(e.store.attempts(jid)),
                               "committed_usd": e.store.ledger_summary(jid)["committed_usd"]}
            assert e.state(jid) == "accepted"
        return out
    finally:
        e.close()


def backup_restore(tmp: Path):
    from product import admin, config
    from product.tests.support import Env
    e = Env()
    try:
        jid = e.submit("image")
        e.drain()
        arc = tmp / "backup.tar.gz"
        admin.backup(e.s, arc)
        rep = admin.restore(arc, tmp / "restored")
        assert rep["integrity"] == "ok" and rep["jobs"] == 1 and rep["asset_files_present"] == rep["assets"], rep
        return rep
    finally:
        e.close()


def main():
    tmp = Path(tempfile.mkdtemp(prefix="mi-smoke-"))
    try:
        step("media engine on this host")(lambda: media_engine(tmp))
        step("dry image + film jobs through the product")(lambda: dry_jobs(tmp))
        step("backup and restore")(lambda: backup_restore(tmp))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for name, st, detail in RESULTS:
        print(f"{st:4}  {name}\n      {json.dumps(detail, default=str)[:900] if st == 'PASS' else detail}")
    sys.exit(0 if all(r[1] == "PASS" for r in RESULTS) else 1)


if __name__ == "__main__":
    main()
