"""Render every candidate layout for one piece of copy on one picture, with checks and ranking. No network, no spend.

python -m product.typeset.demo --out /tmp/ts --format 4:5 --kind poster --plate plate.png --product-box 0.13 0.18 0.86 0.86 \\
    --logo logo.png --headline "Room for the long way home." --small "mokobara.com" --moods premium calm travel
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from product.typeset import engine as E
from product.typeset import picker


def run(*, out: Path, fmt: str, kind: str, copy: list, kit: E.BrandKit, plate: Path | None, product_box: list | None,
        sheet_cols: int = 4) -> list:
    out.mkdir(parents=True, exist_ok=True)
    cands = picker.candidates(kit=kit, fmt=fmt, kind=kind, copy=copy, plate=plate, product_box_norm=product_box)
    rows = []
    for rank, c in enumerate(cands, 1):
        name = f"{kind}-{fmt.replace(':', 'x')}-{rank:02d}-{c['template']}-{c['system']}.png"
        rec = {k: c[k] for k in ("template", "system", "fmt", "score", "checks", "error")}
        rec["rank"], rec["file"] = rank, name if c["layout"] else None
        if c["layout"]:
            c["layout"]["image"].save(out / name)
            rec["elements"] = [{"role": e.role, "family": e.family, "weight": e.weight, "size": e.size, "lines": e.lines,
                                "colour": e.colour, "box": list(e.box)} for e in c["layout"]["elements"]]
        rows.append(rec)
    (out / "candidates.json").write_text(json.dumps([r for r in rows if r["file"]], indent=1))
    (out / "all-results.json").write_text(json.dumps(rows, indent=1))
    sheet(out, [r for r in rows if r["file"]], out / f"sheet-{kind}-{fmt.replace(':', 'x')}.png", cols=sheet_cols)
    return rows


def sheet(d: Path, rows: list, dest: Path, cols: int = 4, width: int = 360):
    ims = [Image.open(d / r["file"]) for r in rows]
    if not ims:
        return None
    h = int(width * ims[0].height / ims[0].width)
    lab = 44
    rws = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * (width + 12) + 12, rws * (h + lab + 12) + 12), (235, 233, 228))
    d_ = ImageDraw.Draw(S)
    f = ImageFont.truetype(str(E.font_file("inter", 500)), 15)
    for i, (im, r) in enumerate(zip(ims, rows)):
        x = 12 + (i % cols) * (width + 12)
        y = 12 + (i // cols) * (h + lab + 12)
        S.paste(im.resize((width, h), Image.LANCZOS), (x, y))
        blk = [c["check_id"] for c in r["checks"] if c["blocking"]]
        d_.text((x, y + h + 4), f"#{r['rank']} {r['template']} · {r['system']}", font=f, fill=(20, 20, 20))
        d_.text((x, y + h + 23), f"score {r['score']}" + (f" · FAIL {','.join(blk)}" if blk else ""), font=f,
                fill=(170, 30, 30) if blk else (90, 90, 90))
    S.save(dest)
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--format", default="4:5")
    ap.add_argument("--kind", default="poster", choices=["poster", "endcard"])
    ap.add_argument("--plate", type=Path)
    ap.add_argument("--product-box", type=float, nargs=4)
    ap.add_argument("--logo", type=Path)
    ap.add_argument("--headline", required=True)
    ap.add_argument("--sub")
    ap.add_argument("--small")
    ap.add_argument("--moods", nargs="*", default=[])
    ap.add_argument("--system")
    ap.add_argument("--primary", default="#101820")
    ap.add_argument("--background", default="#F4F1EA")
    a = ap.parse_args()
    copy = [{"id": "C01", "text": a.headline, "role": "headline"}]
    if a.sub:
        copy.append({"id": "C02", "text": a.sub, "role": "sub"})
    if a.small:
        copy.append({"id": "C03", "text": a.small, "role": "small"})
    kit = E.BrandKit(primary=a.primary, ink=a.primary, background=a.background, logo=a.logo, system=a.system, moods=a.moods)
    rows = run(out=a.out, fmt=a.format, kind=a.kind, copy=copy, kit=kit, plate=a.plate, product_box=a.product_box)
    for r in rows[:10]:
        print(r["rank"], r["template"], r["system"], r["score"], r["error"] or "")


if __name__ == "__main__":
    main()
