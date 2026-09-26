#!/usr/bin/env python3
"""Render every prompt of arms A, B and C for one brief, exactly as the models will receive them.

    python3 render_prompts.py <brief_id> [--librarian-json path] [--understanding-json path] [--out file.md]

The templates are read from TEST-FLOWS.md (the fenced block after each named heading), so the rendered text can't
drift from the approved design. The Canon block and checklist come from canon_context.py. Without
--librarian-json, the C2 Canon block shows an empty claims list. Without --understanding-json, B2 shows a
placeholder.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TF = (HERE / "TEST-FLOWS.md").read_text()
FENCE = "`" * 3
MEDIA = {
    "S1_product_ad": ("Nano Banana 2 (image, with reference photos)", "stills"),
    "S2_edit": ("Nano Banana 2 edit", "edit"),
    "M1_animate": ("Veo 3.1 Fast image-to-video", "veo"),
    "M2_product_film": ("Veo 3.1 Fast (8-second scenes from approved stills)", "veo"),
    "F1_story_film": ("Veo 3.1 Fast (8-second scenes with native audio; first frames by Nano Banana 2)", "veo"),
}


def block(heading: str) -> str:
    i = TF.index(heading)
    j = TF.index(FENCE, i) + 3
    j = TF.index("\n", j) + 1
    return TF[j:TF.index(FENCE, j)].rstrip("\n")


def style(kind: str) -> str:
    sec = TF[TF.index("## 5. Model style guides"):]
    sec = sec[:sec.index("\n---")]
    key = {"stills": "- **Stills**", "edit": "- **Edit:**", "veo": "- **Veo 3.1:**"}[kind]
    i = sec.index(key)
    nxt = [sec.index(k, i + 1) for k in ("\n- **Stills**", "\n- **Edit:**", "\n- **Veo 3.1:**") if k in sec[i + 1:]]
    return sec[i:min(nxt) if nxt else len(sec)].strip()


def canon(*args: str) -> str:
    return subprocess.run([sys.executable, str(HERE / "canon_context.py"), *args], capture_output=True, text=True, check=True).stdout.strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("brief_id")
    ap.add_argument("--librarian-json")
    ap.add_argument("--understanding-json")
    ap.add_argument("--out")
    a = ap.parse_args()
    d = yaml.safe_load((HERE / "BRIEFS.yaml").read_text())
    b = next(x for x in d["exam"] + d["practice"] if x["id"] == a.brief_id)
    cls, brief, answers = b["class"], (b.get("verbatim") or "").strip(), (b.get("answers") or "").strip()
    n_photos = len(b.get("assets") or [])
    model, kind = MEDIA[cls]
    dur = 15 if cls.startswith(("F1", "M2")) else (8 if cls == "M1_animate" else 0)
    photos_line = (f"{n_photos} attached as references — the product must look exactly like them; never describe it at length."
                   if n_photos else "none supplied — invent the food/product look yourself, and keep it identical across scenes by "
                   "repeating one fixed description word for word.")
    understanding = Path(a.understanding_json).read_text().strip() if a.understanding_json else "{produced at run time by B1}"

    A1 = (block("**A1 prompt (writer):**").replace("{brief_verbatim}", brief)
          .replace("{answers_if_any}", f"ANSWERS: {answers}" if answers else "")
          .replace("{n}", str(n_photos)).replace("{media_model_name}", model)
          .replace("{format_line}", "Format: vertical 9:16, 15 seconds." if dur == 15 else "")
          .replace("{duration}", str(dur or 15)).replace("{scene_len}", "8"))
    A3 = block("**A3 prompt (pick):**").replace("{brief_verbatim}", brief)
    B1 = (block("**B1 prompt (understand):**").replace("{brief_verbatim}", brief).replace("{answers}", answers or "none")
          .replace("{photo_descriptions_or_count}", f"{n_photos} photo(s)" if n_photos else "none supplied"))
    B2 = (block("**B2 prompt (writer):**").replace("{brief_verbatim}", brief).replace("{answers}", answers or "none")
          .replace("{B1 json}", understanding).replace("{photos_line}", photos_line)
          .replace("{media_model_name}", model).replace("{style_guide_for_class}", style(kind)))
    lint = block("**The lint message returned to the writer:**")
    bfile = HERE / f".brief-{a.brief_id}.txt"
    bfile.write_text(brief + (f"\nANSWERS: {answers}" if answers else "")
                     + ("\nPHOTOS: " + ", ".join(b["assets"]) if b.get("assets") else "\nPHOTOS: none supplied"))
    lib = canon("librarian", str(bfile), cls)
    bfile.unlink()
    lib_short = (lib[:lib.index("GAP RULES:") + 10] + "\n… (the 25 gap-card rules, numbered G1–G25 — canon/shape-v1/GAP-CARD.md)\n\nINDEX:"
                 + "\n… (the 1,300-line label index — canon/shape-v1/LABEL-INDEX.md)")
    picks = json.loads(Path(a.librarian_json).read_text()) if a.librarian_json else {}
    ids, gaps = picks.get("ids", []), [str(g).lstrip("G") for g in picks.get("gap_rules", [])]
    C2 = B2.replace("Do this in order:", canon("block", cls, ",".join(ids), ",".join(gaps)) + "\n\nDo this in order:")
    C2b = block("### 4.4 C2b").replace("{AFTER-WRITING-CHECKLIST.yaml questions C01–C15}", canon("checklist"))

    f = lambda t: f"{FENCE}\n{t}\n{FENCE}"
    out = "\n\n".join([
        f"# Every prompt, rendered for {a.brief_id} ({cls})",
        "Rendered by `render_prompts.py` from `TEST-FLOWS.md` + `canon_context.py`. This is exactly what each model receives.",
        "## ARM A: LLM + media model", "### A1 → writer", f(A1), "### A3 → writer (pick, after generation)", f(A3),
        "## ARM B: our pipeline", "### B1 → understand model", f(B1), "### B2 → writer", f(B2),
        "### B3 → lint message (only if code flags something)", f(lint), "(B6 pick = the same as A3.)",
        "## ARM C: LLM + Canon + our pipeline", "### C0 → librarian (the full label index is appended)", f(lib_short),
        "**Librarian picks used below:** gap rules " + (", ".join("G" + g for g in gaps) or "none") + "; claims " + (", ".join(ids) if ids else "(none — run C0 first)"),
        "### C2 → writer (the B2 prompt with the Canon block inserted — the complete prompt)", f(C2),
        "### C2b → the same writer, after its draft", f(C2b),
    ])
    if a.out:
        Path(a.out).write_text(out + "\n")
    print(out if not a.out else f"wrote {a.out}: {len(out.split())} words (C2 {len(C2.split())}, B2 {len(B2.split())}, A1 {len(A1.split())})")


if __name__ == "__main__":
    main()
