#!/usr/bin/env python3
"""
EVAL-003 · Build the BLINDED Hindi-reader review pack from the candidate manifest.

Blinding is the whole point. The reviewer must write down what is visibly drawn, not what they
think was intended. A reader shown an expected answer is subject to exactly the auto-correction
pull that made one AI checker report six visibly misspelled signs as correct.

So the generated pack contains ONLY: item id, source image path, crop box.
It contains NO source transcription, NO checker output, NO expected answer.
`--verify-blind` re-reads the generated files and fails if any Devanagari character appears.

No image is copied or modified: the viewer crops from the original at display time, so there is
no transformed-file provenance risk and no storage cost.
"""
import argparse, csv, json, unicodedata
from pathlib import Path

DEV = lambda s: any(0x0900 <= ord(c) <= 0x097F for c in s)

VIEWER = """<!doctype html>
<meta charset="utf-8">
<title>Devanagari calibration — blind transcription pass</title>
<style>
 body{font:15px/1.5 system-ui,sans-serif;margin:0;background:#111;color:#eee}
 header{padding:12px 20px;background:#1c1c1c;border-bottom:1px solid #333;position:sticky;top:0}
 .wrap{max-width:900px;margin:0 auto;padding:20px}
 .crop{background:#000;border:1px solid #444;overflow:hidden;margin:14px 0;
       display:flex;align-items:center;justify-content:center;min-height:220px}
 .crop img{image-rendering:auto;display:block}
 label{display:block;margin:10px 0 4px;color:#bbb;font-size:13px}
 input[type=text]{width:100%;padding:10px;font-size:20px;background:#000;color:#fff;
                  border:1px solid #555;border-radius:4px}
 .row{display:flex;gap:16px;align-items:center;margin:10px 0}
 button{padding:9px 16px;font-size:14px;background:#2b6;color:#000;border:0;border-radius:4px;cursor:pointer}
 button.sec{background:#444;color:#eee}
 .meta{color:#888;font-size:12px}
 .warn{background:#3a2a00;border:1px solid #764;padding:10px;border-radius:4px;margin:12px 0}
</style>
<header>
  <b>Blind transcription pass</b> &nbsp;<span class=meta id=pos></span>
  <span style="float:right"><button class=sec onclick=exportCsv()>Export CSV</button></span>
</header>
<div class=wrap>
 <div class=warn>
  Write <b>exactly what you can see drawn</b> — letter for letter. Do <b>not</b> correct spelling and
  do <b>not</b> write what you think the sign was meant to say. If it is not readable, use
  <b>cannot read</b>. If it could genuinely be read more than one way, use <b>ambiguous</b> and say
  why. There is no expected answer shown anywhere in this page, and that is deliberate.
 </div>
 <div class=meta id=itemid></div>
 <div class=crop id=crop></div>
 <label>What is visibly written?</label>
 <input type=text id=txt autocomplete=off spellcheck=false>
 <div class=row>
   <label><input type=radio name=st value=transcribed checked> transcribed</label>
   <label><input type=radio name=st value=cannot_read> cannot read</label>
   <label><input type=radio name=st value=ambiguous> ambiguous</label>
 </div>
 <label>Notes (optional)</label>
 <input type=text id=note autocomplete=off>
 <div class=row>
   <button onclick=prev()>&larr; back</button>
   <button onclick=next()>save &amp; next &rarr;</button>
   <span class=meta id=saved></span>
 </div>
</div>
<script>
const ITEMS = __ITEMS__;
const ROOT  = "__ROOT__";
let i = 0, R = JSON.parse(localStorage.getItem("dev_v0_reviews") || "{}");
function show(){
  const it = ITEMS[i];
  document.getElementById("pos").textContent = `item ${i+1} of ${ITEMS.length}`;
  document.getElementById("itemid").textContent = it.item_id;
  const [x0,y0,x1,y1] = it.crop_box_xyxy, w = x1-x0, h = y1-y0;
  const scale = Math.min(3, Math.max(1, 420/Math.max(w,h)));
  document.getElementById("crop").innerHTML =
    `<div style="width:${w*scale}px;height:${h*scale}px;overflow:hidden;position:relative">
       <img src="${ROOT}/${it.source_image_relpath}"
            style="position:absolute;left:${-x0*scale}px;top:${-y0*scale}px;
                   transform-origin:0 0;transform:scale(${scale})">
     </div>`;
  const r = R[it.item_id] || {};
  document.getElementById("txt").value  = r.human_transcription || "";
  document.getElementById("note").value = r.notes || "";
  for (const el of document.getElementsByName("st")) el.checked = (el.value === (r.status || "transcribed"));
  document.getElementById("saved").textContent = Object.keys(R).length + " saved";
}
function save(){
  const it = ITEMS[i];
  R[it.item_id] = {
    item_id: it.item_id,
    human_transcription: document.getElementById("txt").value,
    status: [...document.getElementsByName("st")].find(e=>e.checked).value,
    notes: document.getElementById("note").value,
  };
  localStorage.setItem("dev_v0_reviews", JSON.stringify(R));
}
function next(){ save(); if(i<ITEMS.length-1){i++; show();} else { show(); alert("End of pack. Use Export CSV."); } }
function prev(){ save(); if(i>0){i--; show();} }
function exportCsv(){
  save();
  const rows = [["item_id","human_transcription","status","notes"]];
  for (const it of ITEMS){ const r=R[it.item_id]||{};
    rows.push([it.item_id, r.human_transcription||"", r.status||"", (r.notes||"").replace(/"/g,'""')]); }
  const csv = rows.map(r=>r.map(c=>`"${c}"`).join(",")).join("\\n");
  const a=document.createElement("a");
  a.href=URL.createObjectURL(new Blob(["\\ufeff"+csv],{type:"text/csv;charset=utf-8"}));
  a.download="human-responses-devanagari-v0.csv"; a.click();
}
show();
</script>
"""

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    here = Path(__file__).resolve().parent
    ap.add_argument("--manifest", default=str(here / "candidate-manifest.jsonl"))
    ap.add_argument("--out-dir", default=str(here / "review-pack"))
    ap.add_argument("--image-root", default="../../../../resources/resources/corpus/raw",
                    help="path the viewer uses to reach the original images, relative to the "
                         "generated HTML. The raw corpus is git-ignored and may live elsewhere.")
    ap.add_argument("--verify-blind", action="store_true",
                    help="re-read the generated pack and fail if any Devanagari leaked into it")
    a = ap.parse_args()

    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(l) for l in Path(a.manifest).read_text(encoding="utf-8").splitlines() if l.strip()]

    # BLIND PROJECTION — id, image, box. Nothing else crosses this boundary.
    blind = [{"item_id": r["candidate_id"],
              "source_image_relpath": r["source_image_relpath"],
              "crop_box_xyxy": r["crop_box_xyxy"]} for r in rows]

    (out / "items-blind.json").write_text(json.dumps(blind, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "index.html").write_text(
        VIEWER.replace("__ITEMS__", json.dumps(blind, ensure_ascii=False))
              .replace("__ROOT__", a.image_root), encoding="utf-8")

    with open(out / "human-response-template.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["item_id", "human_transcription", "status", "notes"])
        for b in blind:
            w.writerow([b["item_id"], "", "", ""])   # status: transcribed | cannot_read | ambiguous

    (out / "RESPONSE-SCHEMA.json").write_text(json.dumps({
        "description": "Response format for the blind Devanagari transcription pass (EVAL-003).",
        "one_row_per": "candidate item",
        "fields": {
            "item_id": "must match a candidate_id in candidate-manifest.jsonl",
            "human_transcription": "exactly what is visibly drawn, letter for letter, Unicode preserved. "
                                   "Empty if status is cannot_read.",
            "status": "transcribed | cannot_read | ambiguous",
            "notes": "free text; required when status is ambiguous",
        },
        "IMPORTANT": "These readings become the reference for scoring checkers. They do NOT become "
                     "project ground truth about what the sign 'really' says — see HUMAN-REVIEW-GUIDE.md.",
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"wrote blind pack for {len(blind)} items -> {out}")

    if a.verify_blind:
        leaks = []
        for f in sorted(out.iterdir()):
            if not f.is_file():
                continue
            t = f.read_text(encoding="utf-8", errors="replace")
            bad = sorted({c for c in t if DEV(c)})
            if bad:
                leaks.append((f.name, "".join(bad)[:40]))
        if leaks:
            print("BLINDING FAILED — Devanagari found in generated pack:")
            for n, ch in leaks:
                print(f"   {n}: {ch}")
            raise SystemExit(1)
        print("BLINDING VERIFIED — no Devanagari character appears anywhere in the generated pack.")
        print("   (the reviewer therefore cannot be cued by an expected answer)")

if __name__ == "__main__":
    main()
