#!/usr/bin/env python3
"""
Build a single self-contained HTML review packet from the existing native-validation sheets.

WHAT THIS IS
    A review *interface* only. It changes nothing about the battery: no new words, no new items, no
    threshold, no design decision. It takes the three approved sheets in `native-validation/` and
    the images the deterministic build already produced, and presents them one at a time to one
    Hindi-competent reader, with the answer columns **blank**.

WHY A SINGLE HTML FILE
    The reviewer should double-click a file and start. No server, no install, no network. Images are
    embedded as data URIs so the packet is one artifact that can be copied anywhere. Answers are
    kept in the browser's local storage as they go, so the reviewer can stop and resume, and are
    exported as CSVs whose headers and row order match the source sheets exactly — so results import
    back mechanically rather than by hand.

WHAT IT MUST NOT DO
    Pre-fill an answer, reorder or renumber anything, or invent an item. Stable ids (`word_id`,
    `pair_id`, image path) are carried through untouched: they are how a completed sheet is matched
    back to the battery, and they must survive the word list being expanded later.

    It also does not ask the reviewer to read the perceptibility images. That task is "can you see a
    difference between these two pictures", and the two panels are labelled Image 1 / Image 2 for
    exactly that reason.

Usage:
    python3 build_items.py --total 120
    python3 make_validation_sheets.py --from-build build
    python3 make_review_packet.py --from-build build      # writes build/review-packet/
    python3 make_review_packet.py --from-build build --verify

The packet is written under `build/`, which is git-ignored: it embeds rendered images and is fully
reproducible from committed code. No network, no model, no spend.
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import html
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The answer values each section may record. These are the values the existing sheets document,
# and the export writes them verbatim into the sheet's own answer column.
WORD_CHOICES = [("yes", "YES — real / well-formed Hindi as written"),
                ("no", "NO"),
                ("unsure", "UNSURE")]
PAIR_CHOICES = [("yes", "YES — difference clearly visible"),
                ("close", "ONLY WHEN LOOKING CLOSELY"),
                ("no", "NO — cannot see a difference")]
SANITY_CHOICES = [("yes", "NORMAL"),
                  ("no", "BROKEN / SUSPICIOUS")]

# Sheet name -> (source csv, answer column, id column)
SHEETS = {
    "words": ("word-validation-sheet.csv", "is_real_wellformed_hindi_word", "word_id"),
    "pairs": ("perceptibility-sheet.csv", "can_you_see_a_difference", "pair_id"),
    "sanity": ("rendering-sanity-sheet.csv", "looks_like_normal_hindi_text", "image"),
}


def read_sheet(path: Path) -> tuple[list[str], list[dict]]:
    with open(path, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), list(r)


def data_uri(p: Path) -> str:
    if not p.exists():
        raise SystemExit(
            f"missing image: {p}\n"
            f"The sheets reference images the build has not produced. Run, in this order:\n"
            f"    python3 build_items.py --total 120\n"
            f"    python3 make_validation_sheets.py --from-build build\n"
            f"    python3 make_review_packet.py --from-build build")
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("ascii")


def load(sheet_dir: Path, build_dir: Path) -> dict:
    out = {"sheets": {}, "images": {}}
    for key, (name, answer_col, id_col) in SHEETS.items():
        header, rows = read_sheet(sheet_dir / name)
        assert answer_col in header, f"{name} is missing its answer column {answer_col!r}"
        out["sheets"][key] = {"file": name, "header": header, "rows": rows,
                              "answer_col": answer_col, "id_col": id_col}
    # Embed only the images the sheets actually reference.
    for r in out["sheets"]["pairs"]["rows"]:
        for col in ("image_a", "image_b"):
            rel = r[col]
            out["images"].setdefault(rel, data_uri(build_dir / rel))
    for r in out["sheets"]["sanity"]["rows"]:
        rel = r["image"]
        out["images"].setdefault(rel, data_uri(build_dir / rel))
    return out


def packet_fingerprint(data: dict) -> str:
    """Identifies this exact packet, so saved progress is never reused across a rebuild."""
    h = hashlib.sha256()
    for key in ("words", "pairs", "sanity"):
        s = data["sheets"][key]
        h.update(s["file"].encode())
        for r in s["rows"]:
            h.update(r[s["id_col"]].encode("utf-8"))
    return h.hexdigest()[:16]


# --------------------------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------------------------
CSS = """
:root{--bg:#faf9f7;--fg:#1c1a17;--muted:#6b665e;--line:#e2ded7;--card:#fff;
--accent:#2f5d50;--accent-fg:#fff;--warn:#8a5a1b}
@media (prefers-color-scheme:dark){:root{--bg:#16150f;--fg:#eceae4;--muted:#9d968a;
--line:#332f27;--card:#1e1c16;--accent:#7fb3a0;--accent-fg:#10201b;--warn:#d9a441}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
header{border-bottom:1px solid var(--line);padding:14px 22px;position:sticky;top:0;
background:var(--bg);z-index:5}
h1{font-size:17px;margin:0 0 4px;font-weight:600;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:13px}
nav{display:flex;gap:6px;margin-top:12px;flex-wrap:wrap}
nav button{border:1px solid var(--line);background:var(--card);color:var(--fg);
padding:7px 14px;border-radius:999px;cursor:pointer;font-size:13px;font-weight:500}
nav button[aria-current="true"]{background:var(--accent);color:var(--accent-fg);
border-color:var(--accent)}
main{max-width:840px;margin:0 auto;padding:26px 22px 90px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:26px}
.q{color:var(--muted);font-size:14px;margin:0 0 18px}
.word{font-size:64px;line-height:1.35;text-align:center;margin:26px 0 30px;word-break:break-word}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:8px 0 26px}
.pane{border:1px solid var(--line);border-radius:10px;padding:12px;background:var(--bg);
text-align:center}
.pane span{display:block;font-size:11px;letter-spacing:.09em;text-transform:uppercase;
color:var(--muted);margin-bottom:9px}
.pane img,.single img{max-width:100%;height:auto;image-rendering:pixelated;
background:#fff;border-radius:4px}
.single{text-align:center;margin:8px 0 26px}
.choices{display:flex;flex-direction:column;gap:9px}
.choices button{text-align:left;padding:14px 17px;border-radius:10px;border:1.5px solid var(--line);
background:var(--bg);color:var(--fg);font-size:15px;cursor:pointer;display:flex;
justify-content:space-between;align-items:center;gap:12px}
.choices button:hover{border-color:var(--accent)}
.choices button[aria-pressed="true"]{background:var(--accent);color:var(--accent-fg);
border-color:var(--accent);font-weight:600}
.choices kbd{border:1px solid currentColor;border-radius:4px;padding:0 6px;font-size:11px;
opacity:.55;font-family:ui-monospace,monospace}
textarea{width:100%;margin-top:16px;padding:11px;border:1px solid var(--line);border-radius:9px;
background:var(--bg);color:var(--fg);font:inherit;font-size:14px;resize:vertical;min-height:56px}
.foot{display:flex;justify-content:space-between;align-items:center;gap:14px;margin-top:22px}
.foot button{padding:10px 20px;border-radius:9px;border:1px solid var(--line);
background:var(--card);color:var(--fg);cursor:pointer;font-size:14px}
.foot button:disabled{opacity:.35;cursor:default}
.count{color:var(--muted);font-size:13px;font-variant-numeric:tabular-nums}
.bar{height:3px;background:var(--line);border-radius:2px;overflow:hidden;margin:14px 0 0}
.bar i{display:block;height:100%;background:var(--accent);transition:width .18s}
.meta{color:var(--muted);font-size:12px;margin-top:16px;font-family:ui-monospace,monospace}
.done{text-align:center;padding:14px 0}
.done h2{font-size:20px;margin:0 0 8px}
.exports{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:20px}
.exports button{padding:11px 18px;border-radius:9px;border:1px solid var(--accent);
background:var(--accent);color:var(--accent-fg);cursor:pointer;font-size:14px;font-weight:600}
.exports button.sec{background:var(--card);color:var(--fg);border-color:var(--line);
font-weight:500}
.note{background:var(--bg);border:1px solid var(--line);border-left:3px solid var(--warn);
border-radius:8px;padding:13px 15px;font-size:13.5px;color:var(--muted);margin-top:22px}
.skip{color:var(--muted);font-size:13px;background:none;border:none;cursor:pointer;
text-decoration:underline;padding:0}
@media(max-width:640px){.pair{grid-template-columns:1fr}.word{font-size:46px}}
"""

JS = r"""
const SEC = [
  {key:'words', title:'Words', n:DATA.sheets.words.rows.length,
   q:'Is this a real, well-formed Hindi word as written?', choices:CHOICES.words},
  {key:'pairs', title:'Image pairs', n:DATA.sheets.pairs.rows.length,
   q:'Can you see a difference between these two images? You are not being asked to read them.',
   choices:CHOICES.pairs},
  {key:'sanity', title:'Rendering', n:DATA.sheets.sanity.rows.length,
   q:'Does this look like normal, correctly formed Hindi text?', choices:CHOICES.sanity},
];
const KEY = 'eval005-review-' + DATA.fingerprint;
let answers = {words:{}, pairs:{}, sanity:{}};
try { const s = localStorage.getItem(KEY); if (s) answers = JSON.parse(s); } catch (e) {}
let si = 0, ix = {words:0, pairs:0, sanity:0};

const save = () => { try { localStorage.setItem(KEY, JSON.stringify(answers)); } catch(e){} };
const rowsOf = k => DATA.sheets[k].rows;
const idOf = (k,r) => r[DATA.sheets[k].id_col];
const answered = k => rowsOf(k).filter(r => (answers[k][idOf(k,r)]||{}).answer).length;
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function render(){
  document.getElementById('nav').innerHTML = SEC.map((s,i)=>
    `<button data-s="${i}" aria-current="${i===si}">${s.title} · ${answered(s.key)}/${s.n}</button>`
  ).join('') + `<button data-s="${SEC.length}" aria-current="${si===SEC.length}">Export</button>`;

  const main = document.getElementById('main');
  // The export view has no section behind it, so this must come before any SEC[si] access.
  if (si === SEC.length){ main.innerHTML = exportView(); wire(); return; }

  const sec = SEC[si], k = sec.key, rows = rowsOf(k);
  const i = Math.min(ix[k], rows.length-1), row = rows[i], id = idOf(k,row);
  const cur = answers[k][id] || {};
  let body = '';
  if (k === 'words'){
    body = `<div class="word" lang="hi">${esc(row.word)}</div>`;
  } else if (k === 'pairs'){
    body = `<div class="pair">
      <div class="pane"><span>Image 1</span><img alt="" src="${DATA.images[row.image_a]}"></div>
      <div class="pane"><span>Image 2</span><img alt="" src="${DATA.images[row.image_b]}"></div>
    </div>`;
  } else {
    body = `<div class="single"><img alt="" src="${DATA.images[row.image]}"></div>`;
  }

  main.innerHTML = `<div class="card">
    <p class="q">${esc(sec.q)}</p>
    ${body}
    <div class="choices">${sec.choices.map(([v,label],n)=>
      `<button data-a="${v}" aria-pressed="${cur.answer===v}">${esc(label)}<kbd>${n+1}</kbd></button>`
    ).join('')}</div>
    <textarea id="note" placeholder="Optional note (leave empty if you have none)">${esc(cur.note||'')}</textarea>
    <div class="foot">
      <button id="prev" ${i===0?'disabled':''}>&larr; Back</button>
      <span class="count">${i+1} of ${rows.length}${cur.answer?'':' · not answered'}</span>
      <button id="next">${i===rows.length-1?'Finish section':'Skip / Next'} &rarr;</button>
    </div>
    <div class="bar"><i style="width:${100*answered(k)/rows.length}%"></i></div>
    <div class="meta">${esc(DATA.sheets[k].id_col)}: ${esc(id)}</div>
  </div>`;
  wire();
}

function exportView(){
  const total = SEC.reduce((a,s)=>a+s.n,0), done = SEC.reduce((a,s)=>a+answered(s.key),0);
  return `<div class="card done">
    <h2>${done} of ${total} answered</h2>
    <p class="q">${SEC.map(s=>`${s.title} ${answered(s.key)}/${s.n}`).join(' &nbsp;·&nbsp; ')}</p>
    <div class="exports">
      <button data-x="all">Download all results (.zip is not used — saves 4 files)</button>
    </div>
    <div class="exports">
      <button class="sec" data-x="words">word-validation-sheet.csv</button>
      <button class="sec" data-x="pairs">perceptibility-sheet.csv</button>
      <button class="sec" data-x="sanity">rendering-sanity-sheet.csv</button>
      <button class="sec" data-x="json">eval-005-review-results.json</button>
    </div>
    <div class="note"><b>Unanswered items export as blank</b>, exactly as they arrived — nothing is
    guessed or filled in on your behalf. You can download partway through, close the page and come
    back; your answers are kept in this browser until you clear them.
    <br><br><button class="skip" data-x="reset">Clear my answers and start over</button></div>
  </div>`;
}

function csvCell(v){
  v = v == null ? '' : String(v);
  return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g,'""') + '"' : v;
}
function buildCsv(k){
  const s = DATA.sheets[k];
  const lines = [s.header.map(csvCell).join(',')];
  for (const row of s.rows){
    const a = answers[k][row[s.id_col]] || {};
    const out = s.header.map(h =>
      h === s.answer_col ? (a.answer || '') :
      h === 'reader_note' ? (a.note || '') : row[h]);
    lines.push(out.map(csvCell).join(','));
  }
  return lines.join('\n') + '\n';
}
function buildJson(){
  const o = {packet:'eval-005-native-validation', fingerprint:DATA.fingerprint,
             build:DATA.build, exported_at:new Date().toISOString(), sections:{}};
  for (const k of Object.keys(DATA.sheets)){
    const s = DATA.sheets[k];
    o.sections[k] = {sheet:s.file, id_field:s.id_col, answer_field:s.answer_col,
      responses: s.rows.map(r => {
        const a = answers[k][r[s.id_col]] || {};
        return {id:r[s.id_col], answer:a.answer || '', note:a.note || ''};
      })};
  }
  return JSON.stringify(o, null, 2);
}
function download(name, text, mime){
  const b = new Blob([text], {type:mime}), u = URL.createObjectURL(b);
  const a = document.createElement('a');
  a.href = u; a.download = name; document.body.appendChild(a); a.click();
  a.remove(); setTimeout(()=>URL.revokeObjectURL(u), 1000);
}
function doExport(what){
  const files = {words:'word-validation-sheet.csv', pairs:'perceptibility-sheet.csv',
                 sanity:'rendering-sanity-sheet.csv'};
  if (what === 'json'){ download('eval-005-review-results.json', buildJson(), 'application/json'); return; }
  if (what === 'reset'){
    if (confirm('Clear every answer you have given? This cannot be undone.')){
      answers = {words:{}, pairs:{}, sanity:{}}; save(); render();
    }
    return;
  }
  if (what === 'all'){
    Object.keys(files).forEach((k,n)=> setTimeout(()=>download(files[k], buildCsv(k), 'text/csv'), n*260));
    setTimeout(()=>download('eval-005-review-results.json', buildJson(), 'application/json'), 800);
    return;
  }
  download(files[what], buildCsv(what), 'text/csv');
}

function wire(){
  document.querySelectorAll('#nav button').forEach(b =>
    b.onclick = () => { si = +b.dataset.s; render(); });
  document.querySelectorAll('[data-x]').forEach(b => b.onclick = () => doExport(b.dataset.x));
  const k = SEC[si] && SEC[si].key;
  if (!k) return;
  const rows = rowsOf(k), i = Math.min(ix[k], rows.length-1), id = idOf(k, rows[i]);
  const note = document.getElementById('note');
  if (note) note.oninput = () => {
    answers[k][id] = Object.assign({}, answers[k][id], {note: note.value}); save();
  };
  document.querySelectorAll('[data-a]').forEach(b => b.onclick = () => {
    const prev = (answers[k][id] || {}).answer;
    answers[k][id] = Object.assign({}, answers[k][id],
                                   {answer: prev === b.dataset.a ? '' : b.dataset.a});
    save();
    const wasBlank = !prev;
    render();
    if (wasBlank && answers[k][id].answer) setTimeout(()=>step(1), 130);
  });
  const p = document.getElementById('prev'), n = document.getElementById('next');
  if (p) p.onclick = () => step(-1);
  if (n) n.onclick = () => step(1);
}
function step(d){
  const k = SEC[si].key, rows = rowsOf(k), i = Math.min(ix[k], rows.length-1) + d;
  if (i < 0) return;
  if (i >= rows.length){ si = Math.min(si+1, SEC.length); render(); return; }
  ix[k] = i; render();
}
document.addEventListener('keydown', e => {
  if (e.target.tagName === 'TEXTAREA') return;
  if (si === SEC.length) return;
  const c = SEC[si].choices;
  if (e.key >= '1' && e.key <= String(c.length)){
    const b = document.querySelector(`[data-a="${c[+e.key-1][0]}"]`); if (b) b.click();
  }
  if (e.key === 'ArrowRight') step(1);
  if (e.key === 'ArrowLeft') step(-1);
});
render();
"""


def build_html(data: dict, fingerprint: str, build_meta: dict) -> str:
    payload = {
        "fingerprint": fingerprint,
        "build": build_meta,
        "images": data["images"],
        "sheets": {k: {"file": v["file"], "header": v["header"], "rows": v["rows"],
                       "answer_col": v["answer_col"], "id_col": v["id_col"]}
                   for k, v in data["sheets"].items()},
    }
    choices = {"words": WORD_CHOICES, "pairs": PAIR_CHOICES, "sanity": SANITY_CHOICES}
    counts = " · ".join(f"{len(data['sheets'][k]['rows'])} {n}" for k, n in
                        (("words", "words"), ("pairs", "image pairs"), ("sanity", "renders")))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EVAL-005 — Hindi review packet</title>
<style>{CSS}</style></head><body>
<header>
  <h1>EVAL-005 — Hindi review packet</h1>
  <div class="sub">{html.escape(counts)} · one question at a time · nothing is pre-filled ·
  keys <b>1</b>/<b>2</b>/<b>3</b> to answer, <b>&larr;</b> <b>&rarr;</b> to move</div>
  <nav id="nav"></nav>
</header>
<main id="main"></main>
<script>
const DATA = {json.dumps(payload, ensure_ascii=False)};
const CHOICES = {json.dumps(choices, ensure_ascii=False)};
{JS}
</script></body></html>
"""


# --------------------------------------------------------------------------------------------
# Verification
# --------------------------------------------------------------------------------------------
def verify(packet: Path, sheet_dir: Path, data: dict) -> int:
    """Prove the packet is faithful to the sheets and carries no answers. Returns a failure count."""
    doc = packet.read_text(encoding="utf-8")
    start = doc.index("const DATA = ") + len("const DATA = ")
    end = doc.index(";\nconst CHOICES", start)
    embedded = json.loads(doc[start:end])
    fails = 0

    def check(name: str, ok: bool, detail: str = "") -> None:
        nonlocal fails
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail and not ok else ""))
        if not ok:
            fails += 1

    for key, (name, answer_col, id_col) in SHEETS.items():
        src_header, src_rows = read_sheet(sheet_dir / name)
        emb = embedded["sheets"][key]

        check(f"{name}: every row appears exactly once",
              len(emb["rows"]) == len(src_rows) and len(src_rows) > 0,
              f"{len(emb['rows'])} vs {len(src_rows)}")
        check(f"{name}: header preserved verbatim", emb["header"] == src_header,
              f"{emb['header']} vs {src_header}")

        src_ids = [r[id_col] for r in src_rows]
        emb_ids = [r[id_col] for r in emb["rows"]]
        check(f"{name}: stable ids preserved, in order and without duplicates",
              emb_ids == src_ids and len(set(emb_ids)) == len(emb_ids))
        check(f"{name}: every embedded row is byte-equal to its source row",
              emb["rows"] == src_rows)
        check(f"{name}: no answer is pre-filled",
              all(not r.get(answer_col) for r in emb["rows"]))
        check(f"{name}: no note is pre-filled",
              all(not r.get("reader_note", "") for r in emb["rows"]))

    # Every referenced image is embedded, and nothing else is.
    referenced = {r[c] for r in data["sheets"]["pairs"]["rows"] for c in ("image_a", "image_b")}
    referenced |= {r["image"] for r in data["sheets"]["sanity"]["rows"]}
    check("every referenced image is embedded, and no extra image is",
          set(embedded["images"]) == referenced,
          f"{len(embedded['images'])} embedded vs {len(referenced)} referenced")
    check("all embedded images are PNG data URIs",
          all(v.startswith("data:image/png;base64,") for v in embedded["images"].values()))

    # The exported CSV must round-trip into the source sheet: same header, same ids, same order,
    # with only the answer and note columns changed. Reproduce the browser's writer in Python.
    def export_csv(key: str, answers: dict) -> str:
        s = embedded["sheets"][key]
        buf = [",".join(_csv_cell(h) for h in s["header"])]
        for row in s["rows"]:
            a = answers.get(row[s["id_col"]], {})
            buf.append(",".join(_csv_cell(
                a.get("answer", "") if h == s["answer_col"] else
                a.get("note", "") if h == "reader_note" else row[h]) for h in s["header"]))
        return "\n".join(buf) + "\n"

    for key, (name, answer_col, id_col) in SHEETS.items():
        src_header, src_rows = read_sheet(sheet_dir / name)
        blank = export_csv(key, {})
        check(f"{name}: exporting with no answers reproduces the source sheet exactly",
              blank == (sheet_dir / name).read_text(encoding="utf-8"))

        # A filled export must parse back with the same header/ids and the answers in place.
        sample = {r[id_col]: {"answer": "yes", "note": 'a note, with a comma and "quotes"'}
                  for r in src_rows}
        filled = export_csv(key, sample)
        import io
        rr = csv.DictReader(io.StringIO(filled))
        back = list(rr)
        check(f"{name}: a filled export parses back with the same header",
              list(rr.fieldnames or []) == src_header)
        check(f"{name}: a filled export parses back with the same ids in the same order",
              [r[id_col] for r in back] == [r[id_col] for r in src_rows])
        check(f"{name}: answers and notes survive the round trip",
              all(r[answer_col] == "yes" and '"quotes"' in r["reader_note"] for r in back))
        check(f"{name}: no other column is altered by the round trip",
              all(all(back[i][h] == src_rows[i][h]
                      for h in src_header if h not in (answer_col, "reader_note"))
                  for i in range(len(src_rows))))

    verify_js(packet, sheet_dir, check)
    return fails


# --------------------------------------------------------------------------------------------
# Headless regression for the packet's own JavaScript
# --------------------------------------------------------------------------------------------
# WHY THIS EXISTS
#     The first generated packet crashed the moment the reviewer opened the Export view:
#     `render()` destructured `SEC[si]` before the branch that handles the export screen, and on
#     the export screen there is no section behind `si`. It was found by opening the packet in a
#     browser, which is not a check that runs again by itself.
#
#     The data checks above could never have caught it — they inspect the embedded rows, not the
#     code that displays them. So the packet's actual script is now executed headlessly through
#     every screen, including the export view, with a minimal DOM stub. If that ordering bug is
#     reintroduced, this fails.
#
#     Node is used only as a JavaScript engine. No network, no package, no install.

_DRIVER = r"""
// Minimal DOM stub: enough to run render() and wire(), nothing more.
const captured = {};
function el(id){ return {
  set innerHTML(v){ captured[id] = v; }, get innerHTML(){ return captured[id] || ""; },
}; }
const nodes = {};
globalThis.document = {
  getElementById: (id) => (nodes[id] = nodes[id] || el(id)),
  querySelectorAll: () => [],
  querySelector: () => null,
  addEventListener: () => {},
  createElement: () => ({ click(){}, remove(){}, style:{} }),
  body: { appendChild(){}, },
};
const store = new Map();
globalThis.localStorage = {
  getItem: (k) => (store.has(k) ? store.get(k) : null),
  setItem: (k, v) => store.set(k, v),
};
globalThis.Blob = function(){}; globalThis.URL = { createObjectURL(){ return "blob:x"; },
                                                  revokeObjectURL(){} };
__SCRIPT__

// Drive every screen, including the export view that used to throw.
const result = { screens: [], errors: [] };
for (let s = 0; s <= SEC.length; s++) {
  try { si = s; render(); result.screens.push({ si: s, html: captured.main || "" }); }
  catch (e) { result.errors.push({ si: s, message: String(e && e.message || e) }); }
}
result.answersAfterRender = JSON.stringify(answers);
try {
  result.csv = { words: buildCsv("words"), pairs: buildCsv("pairs"), sanity: buildCsv("sanity") };
  result.json = buildJson();
} catch (e) { result.errors.push({ stage: "export", message: String(e && e.message || e) }); }
process.stdout.write(JSON.stringify(result));
"""


def verify_js(packet: Path, sheet_dir: Path, check) -> None:
    """Execute the packet's own script through every screen and both exporters."""
    if shutil.which("node") is None:
        check("javascript regression ran (node available)", False,
              "node not found — the export-view crash regression did NOT run")
        return

    doc = packet.read_text(encoding="utf-8")
    script = doc[doc.index("<script>") + len("<script>"):doc.rindex("</script>")]
    with tempfile.TemporaryDirectory() as t:
        driver = Path(t) / "drive.mjs"
        driver.write_text(_DRIVER.replace("__SCRIPT__", script), encoding="utf-8")
        r = subprocess.run(["node", str(driver)], capture_output=True, text=True)
    if r.returncode != 0:
        check("the packet's script runs headlessly", False, r.stderr.strip()[:300])
        return
    res = json.loads(r.stdout)

    check("no screen throws, including the export view",
          not res["errors"], json.dumps(res["errors"])[:300])
    check("every screen renders (3 sections + export)", len(res["screens"]) == 4,
          str(len(res["screens"])))
    export_html = next((s["html"] for s in res["screens"] if s["si"] == 3), "")
    check("the export view renders its download controls",
          'data-x="words"' in export_html and 'data-x="json"' in export_html)
    check("the export view reports 0 of 98 answered before anyone has answered",
          "0 of 98 answered" in export_html, export_html[:160])
    for s in res["screens"][:3]:
        check(f"screen {s['si']} shows no pre-selected answer",
              'aria-pressed="true"' not in s["html"])
    check("merely rendering records no answer",
          json.loads(res["answersAfterRender"]) == {"words": {}, "pairs": {}, "sanity": {}},
          res["answersAfterRender"][:120])

    for key, (name, _, _) in SHEETS.items():
        check(f"{name}: the packet's own exporter reproduces the source sheet byte for byte",
              res["csv"][key] == (sheet_dir / name).read_text(encoding="utf-8"))
    j = json.loads(res["json"])
    total = sum(len(v["responses"]) for v in j["sections"].values())
    check("the JSON export carries all 98 responses, all blank",
          total == 98 and all(not x["answer"] and not x["note"]
                              for v in j["sections"].values() for x in v["responses"]),
          str(total))


def _csv_cell(v) -> str:
    v = "" if v is None else str(v)
    return '"' + v.replace('"', '""') + '"' if any(c in v for c in ',"\n\r') else v


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet-dir", type=Path, default=HERE / "native-validation")
    ap.add_argument("--from-build", type=Path, default=HERE / "build",
                    help="build directory holding images/ and target-render/")
    ap.add_argument("--out-dir", type=Path, default=None,
                    help="default: <build>/review-packet")
    ap.add_argument("--verify", action="store_true",
                    help="check the packet against the sheets and exit")
    a = ap.parse_args()

    out_dir = a.out_dir or (a.from_build / "review-packet")
    out_dir.mkdir(parents=True, exist_ok=True)
    packet = out_dir / "eval-005-review.html"

    data = load(a.sheet_dir, a.from_build)
    fp = packet_fingerprint(data)
    summary_path = a.from_build / "build-summary.json"
    meta = {}
    if summary_path.exists():
        s = json.loads(summary_path.read_text(encoding="utf-8"))
        meta = {"battery": s.get("battery"), "seed": s.get("seed"),
                "render_spec": s.get("render_spec"),
                "font_sha256": s.get("environment_provenance", {}).get("font_sha256"),
                "renderer": s.get("environment_provenance", {}).get("renderer")}

    if not a.verify:
        packet.write_text(build_html(data, fp, meta), encoding="utf-8")
        kb = packet.stat().st_size / 1024
        print(f"wrote {packet}  ({kb:.0f} KB, self-contained)")
        for k, (name, _, _) in SHEETS.items():
            print(f"  {name:32} {len(data['sheets'][k]['rows']):3} items")
        print(f"  embedded images                  {len(data['images']):3}")
        print(f"  packet fingerprint               {fp}")
        print("\nEvery answer column is blank. No human has been asked anything.")
        return 0

    if not packet.exists():
        sys.exit(f"no packet at {packet}; run without --verify first")
    print(f"Verifying {packet}\n")
    fails = verify(packet, a.sheet_dir, data)
    print()
    if fails:
        print(f"FAILED: {fails} check(s)")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
