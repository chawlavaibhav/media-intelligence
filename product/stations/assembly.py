"""The sign painter and the edit (code, no AI): composed stills, supers, end card, music bed and the assembled film.
Ported from v1 (orchestrator nodes) with two v2 changes: every output goes to a NEW path (write-once, spec §7.1 — v1
overwrote the image job's first-cut posters), and brand fonts/colours come from the customer shelf when approved."""
from __future__ import annotations

import json
import shutil
import time
from pathlib import Path

from product import compose, media, verify


def _done(k, job_id, node_id, aid):
    from product.stations.head_cook import _done as done
    return done(k, job_id, node_id, aid)


def _colour_refs(k, job_id) -> list:
    u = k.store.artifact(job_id, "understanding") or {}
    out = []
    for r in u.get("photo_roles", []):
        if r["role"] in ("product_view", "product_detail"):
            a = k.store.asset(r["asset_id"])
            if a and (a["content_type"] or "").startswith("image/"):
                out.append(Path(a["path"]))
    return out


def brand_fonts(k, job_id) -> list:
    """The customer's approved brand font files (newest version of each), recorded as used by this job."""
    job = k.store.job(job_id)
    out = []
    for it in k.shelf.approved(job["account_id"], "brand_font"):
        if it["path"]:
            k.shelf.record_use(job_id, job["account_id"], it["id"], "brand_font")
            out.append(it["path"])
    return out


def compose_still(k, job_id, n, spec, ctx):
    tok = media.BRAND_FONTS.set(tuple(brand_fonts(k, job_id)))
    try:
        return _compose_still(k, job_id, n, spec, ctx)
    finally:
        media.BRAND_FONTS.reset(tok)


def _compose_still(k, job_id, n, spec, ctx):
    from product.stations.head_cook import fid
    plate = k.store.asset(k.store.node(job_id, n["node_id"].replace("ad_", "plate_"))["selected_asset_id"])
    out = k.store.new_output_path(k.job_dir(job_id) / "out", f"cut{ctx['cut']}-{fid(spec['aspect'])}", "png")
    if not media.have_ffmpeg():
        return placeholder_final(k, job_id, n, plate["path"], out, "image/png", ctx)
    pbox = json.loads(plate["meta_json"]).get("product_box")
    src_plate, colour_rows = Path(plate["path"]), []
    photos = _colour_refs(k, job_id)
    if photos:
        matched = k.store.new_output_path(ctx["workdir"], f"{Path(plate['path']).stem}-colour", "png")
        cm = media.colour_match(src_plate, photos, matched)
        applied = {b: r for b, r in cm.items() if r.get("applied")}
        worst = max((r["distance_after"] for r in applied.values()), default=None)
        colour_rows.append({"check_id": "product_colour_match", "control": "PRODUCT_INTACT_AND_FAITHFUL",
                            "status": "PASS" if worst is not None and worst <= 8 else "FLAG", "blocking": False,
                            "detail": "; ".join(f"{b}: distance {r['distance_before']} -> {r['distance_after']} (reference {r['reference_rgb']})"
                                                for b, r in applied.items()) or "no product colour band found on both", "evidence": cm})
        src_plate = matched
    path, checks, layout = compose.still_ad(plate=src_plate, out=out, aspect=spec["aspect"], direction=ctx["recipe"], logo=ctx["logo"],
                                            workdir=ctx["workdir"], product_box_norm=pbox)
    aid = k.store.add_asset(job_id, path=path, kind="image", source="composed", content_type="image/png", node_id=n["node_id"],
                            role="deliverable", cut=ctx["cut"], meta={"format": spec["aspect"], "layout": layout, "plate": plate["id"]})
    verify.record_rows(k.store, job_id, aid, checks + colour_rows, runner="compositor_gates")
    return _done(k, job_id, n["node_id"], aid)


def end_card(k, job_id, n, spec, ctx):
    tok = media.BRAND_FONTS.set(tuple(brand_fonts(k, job_id)))
    try:
        return _end_card(k, job_id, n, spec, ctx)
    finally:
        media.BRAND_FONTS.reset(tok)


def _end_card(k, job_id, n, spec, ctx):
    size = media.FORMAT_PX[spec["aspect"]]
    out = k.store.new_output_path(ctx["workdir"], f"endcard-cut{ctx['cut']}", "png")
    if not media.have_ffmpeg():
        from runtime.loop.synthetic import make_png
        out.write_bytes(make_png(size[0] // 8, size[1] // 8, seed=7))
        aid = k.store.add_asset(job_id, path=out, kind="image", source="composed", content_type="image/png", node_id=n["node_id"], cut=ctx["cut"])
        return _done(k, job_id, n["node_id"], aid)
    path, checks, layout = compose.end_card(out=out, size=size, direction=ctx["recipe"], logo=ctx["logo"], workdir=ctx["workdir"])
    aid = k.store.add_asset(job_id, path=path, kind="image", source="composed", content_type="image/png", node_id=n["node_id"],
                            cut=ctx["cut"], meta={"layout": layout, "checks": checks})
    verify.record_rows(k.store, job_id, aid, checks, runner="compositor_gates")
    return _done(k, job_id, n["node_id"], aid)


def super(k, job_id, n, spec, ctx):  # noqa: A001 — the node kind is called "super"
    tok = media.BRAND_FONTS.set(tuple(brand_fonts(k, job_id)))
    try:
        return _super(k, job_id, n, spec, ctx)
    finally:
        media.BRAND_FONTS.reset(tok)


def _super(k, job_id, n, spec, ctx):
    size = media.FORMAT_PX[spec["aspect"]]
    deck = {c["id"]: c["text"] for c in ctx["recipe"]["copy_deck"]}
    clip = k.store.asset(k.store.node(job_id, f"shot_{spec['shot']}")["selected_asset_id"])
    cm = json.loads(clip["meta_json"])
    out = k.store.new_output_path(ctx["workdir"], f"super-s{spec['shot']}-cut{ctx['cut']}", "png")
    if not media.have_ffmpeg():
        from runtime.loop.synthetic import make_png
        out.write_bytes(make_png(8, 8, seed=3))
        aid = k.store.add_asset(job_id, path=out, kind="image", source="composed", content_type="image/png", node_id=n["node_id"],
                                cut=ctx["cut"], meta={"checks": []})
        return _done(k, job_id, n["node_id"], aid)
    path, checks = compose.super_overlay(out=out, size=size, text=deck.get(spec["copy_id"], ""), clip=Path(clip["path"]),
                                         clip_in=cm.get("in_s", 0.0), use=cm.get("use_s", 3.0), clip_size=size)
    aid = k.store.add_asset(job_id, path=path, kind="image", source="composed", content_type="image/png", node_id=n["node_id"],
                            cut=ctx["cut"], meta={"checks": checks, "shot": spec["shot"], "rendered_text": [deck.get(spec["copy_id"], "")]})
    return _done(k, job_id, n["node_id"], aid)


def assemble(k, job_id, n, spec, ctx):
    recipe = ctx["recipe"]
    shots = [s for s in recipe["shots"] if s["route"] != "END-CARD"]
    segs, t, supers = [], 0.0, []
    for s in shots:
        clip = k.store.asset(k.store.node(job_id, f"shot_{s['n']}")["selected_asset_id"])
        cm = json.loads(clip["meta_json"])
        segs.append({"clip": clip["path"], "in": cm.get("in_s", 0.0), "use": float(s["duration_s"]), "shot": s["n"], "asset": clip["id"]})
        sn = k.store.node(job_id, f"super_{s['n']}")
        if sn and sn["status"] == "done" and sn["selected_asset_id"]:
            supers.append({"png": k.store.asset(sn["selected_asset_id"])["path"], "t_in": round(t + 0.2, 2),
                           "t_out": round(t + float(s["duration_s"]) - 0.1, 2), "shot": s["n"], "asset": sn["selected_asset_id"]})
        t += float(s["duration_s"])
    endcard = k.store.asset(k.store.node(job_id, "end_card")["selected_asset_id"])
    music = k.store.asset(k.store.node(job_id, "music")["selected_asset_id"])
    size = media.FORMAT_PX[spec["aspect"]]
    from product.stations.head_cook import fid
    out = k.store.new_output_path(k.job_dir(job_id) / "out", f"cut{ctx['cut']}-{fid(spec['aspect'])}", "mp4")
    if not media.have_ffmpeg():
        return placeholder_final(k, job_id, n, segs[0]["clip"], out, "video/mp4", ctx, extra={"segments": segs, "supers": supers})
    rep = media.assemble_film(segments=[{**sg, "beat": sg["shot"]} for sg in segs], endcard=Path(endcard["path"]), supers=supers,
                              music=Path(music["path"]), out=out, size=size, card_s=float(spec["card_s"]),
                              workdir=ctx["workdir"] / f"assemble-cut{ctx['cut']}-{int(time.time() * 1000)}")
    aid = k.store.add_asset(job_id, path=out, kind="video", source="composed", content_type="video/mp4", node_id=n["node_id"],
                            role="deliverable", cut=ctx["cut"],
                            meta={"segments": segs, "supers": supers, "assembly": rep, "end_card": endcard["id"], "music": music["id"]})
    rows = [dict(r, check_id="end_card:" + r["check_id"]) for r in json.loads(endcard["meta_json"]).get("checks", [])]
    for sp in supers:
        for r in json.loads(k.store.asset(sp["asset"])["meta_json"]).get("checks", []):
            rows.append(dict(r, check_id=f"super:s{sp['shot']}:{r['check_id']}"))
    cut_rows = [json.loads(k.store.asset(sg["asset"])["meta_json"]).get("det", {}) for sg in segs]
    worst = "FAIL" if any(r.get("status") == "FAIL" for r in cut_rows) else ("NOT_VERIFIED" if any(r.get("status") != "PASS" for r in cut_rows) else "PASS")
    rows.append({"check_id": "clips:no_in_model_cut", "control": "IN_MODEL_HARD_CUT", "status": worst,
                 "detail": "; ".join(f"s{sg['shot']}: {r.get('detail')}" for sg, r in zip(segs, cut_rows))})
    verify.record_rows(k.store, job_id, aid, rows, runner="compositor_gates+det")
    return _done(k, job_id, n["node_id"], aid)


def placeholder_final(k, job_id, n, src, out, ctype, ctx, extra=None):
    """No media engine on this host: the final is a stand-in and every media check stays NOT_VERIFIED."""
    shutil.copyfile(src, out)
    with open(out, "ab") as fh:
        fh.write(f"\n#cut-{n['node_id']}-{time.time()}".encode())
    aid = k.store.add_asset(job_id, path=out, kind="image" if ctype.startswith("image") else "video", source="composed", content_type=ctype,
                            node_id=n["node_id"], role="deliverable", cut=ctx["cut"],
                            meta={"placeholder": True, "reason": "ffmpeg is not installed on this host", **(extra or {})})
    k.store.record_check(job_id, aid, check_id="media_engine", status="NOT_VERIFIED", blocking=True, runner="system",
                         detail="no media engine on this host: composition/assembly not performed; this file is a stand-in")
    return _done(k, job_id, n["node_id"], aid)
