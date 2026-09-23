"""The founder's taste test: a local page of side-by-side pairs; the founder picks the better one in each pair; the
choices become weights the picker adds to its score (data/taste.yaml), and we measure how often the picker already
agreed with the founder (the compositor's qualification).

  python -m product.typeset.taste page  --dir <candidates dir>            # writes taste.html next to the images
  python -m product.typeset.taste ingest --dir <candidates dir> --results results.json
"""
from __future__ import annotations

import argparse
import html
import itertools
import json
import random
from pathlib import Path

import yaml

from product.typeset import picker

STEP = 2.0          # score points added per net win, per template / type system
CAP = 12.0


def _embed(d: Path, name: str, width: int = 540) -> str:
    """The candidate as an inline JPEG, so the page is one self-contained file the founder can open anywhere."""
    import base64
    import io
    from PIL import Image
    im = Image.open(d / name).convert("RGB")
    im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=86)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def page(d: Path, max_pairs: int = 30, seed: int = 7) -> Path:
    cands = json.loads((d / "candidates.json").read_text())
    ok = [c for c in cands if c["score"] > -1000]
    pairs = list(itertools.combinations(range(len(ok)), 2))
    random.Random(seed).shuffle(pairs)
    pairs = pairs[:max_pairs]
    rows = []
    for k, (a, b) in enumerate(pairs):
        A, B = ok[a], ok[b]
        if random.Random(seed + k).random() < 0.5:
            A, B = B, A
        rows.append(f"""<div class="pair" data-a="{html.escape(A['file'])}" data-b="{html.escape(B['file'])}">
<p>Pair {k + 1} of {len(pairs)} — which is the better ad?</p>
<label><input type="radio" name="p{k}" value="a"><img src="{_embed(d, A['file'])}"></label>
<label><input type="radio" name="p{k}" value="b"><img src="{_embed(d, B['file'])}"></label></div>""")
    doc = f"""<!doctype html><meta charset="utf-8"><title>Layout taste test</title>
<style>body{{font:15px system-ui;margin:24px;background:#f6f5f2}}.pair{{background:#fff;border:1px solid #ddd;border-radius:10px;
padding:12px;margin:0 0 18px}}.pair label{{display:inline-block;width:48%;margin-right:1%;cursor:pointer;vertical-align:top}}
img{{width:100%;border:3px solid transparent;border-radius:6px}}input{{display:none}}input:checked+img{{border-color:#2f6fed}}
textarea{{width:100%;height:120px}}</style>
<h1>Pick the better ad in each pair</h1><p>Judge it as the customer would, at phone size. Then press “Done” and send the text box.</p>
{''.join(rows)}<button onclick="done()">Done</button><textarea id="out"></textarea>
<script>function done(){{const r=[];document.querySelectorAll('.pair').forEach((p,i)=>{{const c=p.querySelector('input:checked');
if(c)r.push({{winner:c.value==='a'?p.dataset.a:p.dataset.b,loser:c.value==='a'?p.dataset.b:p.dataset.a}})}});
document.getElementById('out').value=JSON.stringify(r)}}</script>"""
    out = d / "taste.html"
    out.write_text(doc)
    return out


def ingest(d: Path, results: list, brand: str = "", label: str = "") -> dict:
    """Picks move this brand's weights by STEP and the global weights by STEP/2 (global = what holds across brands;
    round 2 showed some preferences are brand-specific: the dark band lost 1–7 on Mokobara, won 3–1 on Cumin Co.)."""
    cands = {c["file"]: c for c in json.loads((d / "candidates.json").read_text())}
    w = picker.taste_weights()
    targets = [(w, STEP / 2)]
    if brand:
        targets.append((w.setdefault("brands", {}).setdefault(brand, {}), STEP))
    for t, _ in targets:
        t.setdefault("templates", {})
        t.setdefault("systems", {})
    agree = 0
    for r in results:
        win, lose = cands[r["winner"]], cands[r["loser"]]
        agree += win["score"] > lose["score"]
        for t, step in targets:
            for key, field in (("templates", "template"), ("systems", "system")):
                if win[field] != lose[field]:
                    t[key][win[field]] = max(-CAP, min(CAP, t[key].get(win[field], 0.0) + step))
                    t[key][lose[field]] = max(-CAP, min(CAP, t[key].get(lose[field], 0.0) - step))
    w.setdefault("history", []).append({"round": label or str(d), "brand": brand, "pairs": len(results), "picker_agreed": agree})
    picker.TASTE.write_text(yaml.safe_dump(w, sort_keys=True))
    return {"pairs": len(results), "picker_agreed": agree, "agreement": round(agree / len(results), 3) if results else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["page", "ingest"])
    ap.add_argument("--dir", required=True, type=Path)
    ap.add_argument("--results", type=Path)
    ap.add_argument("--brand", default="")
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    if a.cmd == "page":
        print(page(a.dir))
    else:
        print(json.dumps(ingest(a.dir, json.loads(a.results.read_text()), a.brand, a.label), indent=1))


if __name__ == "__main__":
    main()
