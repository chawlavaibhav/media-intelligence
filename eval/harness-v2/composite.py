#!/usr/bin/env python3
"""composite: the deterministic text overlay of TOPO-02 arm C — exact strings set by code onto a textless plate.

    python3 eval/harness-v2/composite.py --run-id <id> --out <dir> --spec <COMPOSITE-SPEC.yaml> [--trial <id> ...]

The plate is a sealed artifact of a `C_composite*` trial (any image format ffmpeg decodes). Every string is
rasterised with the pinned system font FILE and face index through the August exact-text battery's renderer
(`eval/battery/devanagari-exactness/devtext.py`: hb-view, `--unicodes`, transparent background), alpha-blended
onto the plate at the spec's anchor, and the result is sealed under the plate's trial id with suffix
`composite` (media + record + manifest line). USD 0: no provider, no network. Deterministic: same plate + same
spec + same font bytes -> byte-identical output; the spec, the font file sha256 and the renderer version are
recorded in `<out>/COMPOSITE-RECORD.json` next to every composite's sha256.

Layout spec (YAML), one entry per case:
  cases:
    IMG-TEXT-01:
      strings:
        - {id: t1, text: "...", script: devanagari, size_pt: 44, colour: F5E9D3, anchor: center, y_frac: 0.09}
        - {id: t3, text: "...", script: devanagari, size_pt: 96, colour: F5E9D3, anchor: center, y_frac: 0.40}
        - {id: t2, ..., anchor: left, x_frac: 0.06, y_frac: 0.12}
  fonts:
    devanagari: {file: /System/Library/Fonts/Kohinoor.ttc, face_index: 0}
    latin:      {file: /System/Library/Fonts/HelveticaNeue.ttc, face_index: <bold face>}
`y_frac` is the string's vertical CENTRE as a fraction of plate height; `anchor` center|left|right with `x_frac`
for left/right (edge of the text box). Sizes are hb-view point sizes at the plate's native resolution.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

import hv2_paths
import run_live as RL
import store as S
from instruments import imageio as IO

BATTERY_DIR = hv2_paths.REPO_ROOT / "eval" / "battery" / "devanagari-exactness"
sys.path.insert(0, str(BATTERY_DIR))
import devtext  # noqa: E402  (the pinned renderer; hb-view + explicit font file)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def render_text(text: str, font: dict, size_pt: int, colour_hex: str, scratch: Path) -> IO.Image:
    """RGBA glyph image on a transparent ground, via devtext.render (hb-view --unicodes)."""
    out = scratch / f"{_sha(f'{text}|{font}|{size_pt}|{colour_hex}'.encode())[:16]}.png"
    spec = devtext.RenderSpec(font_file=font["file"], face_index=int(font.get("face_index", 0)), point_size=int(size_pt),
                              margin=4, background="00000000", foreground=colour_hex.upper() + "FF")
    devtext.render(text, out, spec)
    img = IO.decode_png(out.read_bytes())
    if img.channels != 4:
        raise RuntimeError(f"expected an RGBA glyph image, got {img.channels} channels")
    return img


def blend(plate: IO.Image, glyphs: IO.Image, x0: int, y0: int) -> IO.Image:
    """Alpha-blend `glyphs` (RGBA) onto `plate` (RGB) with its top-left at (x0, y0); clipped to the plate."""
    W, H, pc = plate.width, plate.height, plate.channels
    if pc != 3:
        raise RuntimeError("plate must be RGB")
    data = bytearray(plate.data)
    gw, gh = glyphs.width, glyphs.height
    g = glyphs.data
    for gy in range(gh):
        y = y0 + gy
        if y < 0 or y >= H:
            continue
        row = gy * gw * 4
        for gx in range(gw):
            x = x0 + gx
            if x < 0 or x >= W:
                continue
            a = g[row + gx * 4 + 3]
            if a == 0:
                continue
            pi = (y * W + x) * 3
            if a == 255:
                data[pi:pi + 3] = g[row + gx * 4:row + gx * 4 + 3]
            else:
                for c in range(3):
                    data[pi + c] = (g[row + gx * 4 + c] * a + data[pi + c] * (255 - a)) // 255
    return IO.Image(W, H, 3, bytes(data))


def place(plate: IO.Image, glyphs: IO.Image, s: dict) -> tuple[int, int]:
    W, H = plate.width, plate.height
    yc = int(round(float(s["y_frac"]) * H))
    y0 = yc - glyphs.height // 2
    anchor = s.get("anchor", "center")
    if anchor == "center":
        x0 = (W - glyphs.width) // 2
    elif anchor == "left":
        x0 = int(round(float(s.get("x_frac", 0.06)) * W))
    elif anchor == "right":
        x0 = int(round(float(s.get("x_frac", 0.94)) * W)) - glyphs.width
    else:
        raise ValueError(f"unknown anchor {anchor!r}")
    return x0, y0


def composite_one(plate_path: Path, case_spec: dict, fonts: dict, scratch: Path) -> tuple[bytes, list[dict]]:
    plate = IO.decode_image_ffmpeg(plate_path)
    placed = []
    for s in case_spec["strings"]:
        font = fonts[s["script"]]
        glyphs = render_text(s["text"], font, s["size_pt"], s["colour"], scratch)
        x0, y0 = place(plate, glyphs, s)
        plate = blend(plate, glyphs, x0, y0)
        placed.append({"id": s["id"], "text": s["text"], "script": s["script"], "size_pt": s["size_pt"], "colour": s["colour"],
                       "box": [x0, y0, glyphs.width, glyphs.height]})
    rows = [plate.data[i * plate.width * 3:(i + 1) * plate.width * 3] for i in range(plate.height)]
    return IO.encode_png(rows, plate.width, plate.height, 3), placed


def run(out: Path | str, run_id: str, spec_path: Path | str, only: set[str] | None = None, suffix: str = "composite") -> dict:
    out = Path(out)
    spec = yaml.safe_load(Path(spec_path).read_text(encoding="utf-8"))
    fonts = spec["fonts"]
    for name, f in fonts.items():
        p = Path(f["file"])
        if not p.exists():
            raise FileNotFoundError(f"font for {name} missing: {p}")
        f["sha256"] = _sha(p.read_bytes())
    plan = RL.load_plan(out, run_id)
    store = S.SealedStore(out / RL.ARTIFACTS_DIR)
    record = {"run_id": run_id, "at": _now(), "suffix": suffix, "spec_path": str(spec_path), "spec_sha256": _sha(Path(spec_path).read_bytes()),
              "fonts": fonts, "renderer": {"module": "eval/battery/devanagari-exactness/devtext.py", "hb_view": _tool_version("hb-view")},
              "usd_spent": 0, "composites": []}
    with tempfile.TemporaryDirectory(prefix="composite-") as td:
        scratch = Path(td)
        for t in plan["trials"]:
            if only and t["trial_id"] not in only:
                continue
            if not str(t["arm"]).startswith("C_composite"):
                continue
            a = store.load_attempt(t["trial_id"])
            if not a or a.get("status") != "ok" or not a.get("artifact"):
                record["composites"].append({"trial_id": t["trial_id"], "skipped": f"no plate artifact ({(a or {}).get('status')})"})
                continue
            case_spec = spec["cases"].get(t["case_id"])
            if not case_spec:
                record["composites"].append({"trial_id": t["trial_id"], "skipped": "no spec for case"})
                continue
            plate_path = store.root / a["artifact"]["relative_path"]
            png, placed = composite_one(plate_path, case_spec, fonts, scratch)
            rec = store.seal(t["trial_id"], png, "image/png", {"derived_from_plate_sha256": a["artifact"]["sha256"], "usd": 0,
                                                            "method": "deterministic overlay (composite.py)", "layout_version": suffix}, suffix=suffix)
            record["composites"].append({"trial_id": t["trial_id"], "case_id": t["case_id"], "plate_sha256": a["artifact"]["sha256"],
                                         "composite_sha256": rec["sha256"], "relative_path": rec["relative_path"], "bytes": rec["bytes"],
                                         "strings": placed})
    (out / f"COMPOSITE-RECORD{'' if suffix == 'composite' else '-' + suffix}.json").write_text(json.dumps(record, indent=1, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    return record


def _tool_version(name: str) -> str | None:
    try:
        r = subprocess.run([name, "--version"], capture_output=True, text=True)
        return (r.stdout or r.stderr).strip().splitlines()[0] if (r.stdout or r.stderr) else None
    except Exception:  # noqa: BLE001
        return None


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--run-id", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--spec", required=True)
    p.add_argument("--trial", action="append", default=None)
    p.add_argument("--suffix", default="composite", help="artifact suffix; a re-layout is sealed under a NEW suffix, never over the old one")
    a = p.parse_args(argv)
    rec = run(a.out, a.run_id, a.spec, set(a.trial) if a.trial else None, suffix=a.suffix)
    print(json.dumps({k: v for k, v in rec.items() if k != "fonts"}, indent=1, ensure_ascii=False))
    return 0 if all("composite_sha256" in c for c in rec["composites"]) else 1


if __name__ == "__main__":
    sys.exit(main())
