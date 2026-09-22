#!/usr/bin/env python3
"""Deterministic prompt builder: Stage 3 form (board) → one still prompt and one motion
prompt per beat, the same shape every time.

    python3 .claude/skills/media-agency/tools/build_prompts.py <job_dir> [--out gen/prompts]

Shape (the accepted Mokobara / V2 shape, made explicit):
  still  = style_line · first_frame (the state at t_in) · [for each anchor the beat restates:
           "The EXACT same <name> as in the reference images — <description>."] ·
           feeling-as-direction · grade · negative_line
  motion = "Image-to-video, <clip_s> s." · framing · impact · audio line · negative_line

Nothing creative is decided here. Every word comes from a form field; change the board
and the prompts change with it. Exact on-screen text never enters a prompt (the copy deck
is composed by code — mechanism B); the builder refuses a board whose beat text contains a
copy-deck string.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_STYLE = "Photorealistic cinematic film still"
DEFAULT_NEGATIVE = "No text, no lettering, no captions, no logos, no watermark anywhere in the image."


def _sentence(s: str) -> str:
    s = s.strip()
    if not s:
        return s
    s = s[0].upper() + s[1:]
    return s if s.endswith((".", "!", "?")) else s + "."


def _anchor_lines(board: dict, beat: dict) -> list[str]:
    anchors = board.get("identity_anchors", {})
    names = beat.get("anchors") or list(anchors.keys())
    out = []
    for name in names:
        desc = anchors.get(name)
        if not desc:
            continue
        if name == "grade":
            out.append(f"Colour: {desc}.")
        else:
            out.append(f"The EXACT same {name} as in the reference images — {desc}.")
    return out


def _guard_copy(text: str, deck_strings: dict, where: str) -> None:
    for sid, s in deck_strings.items():
        if isinstance(s, str) and len(s) >= 3 and not s.endswith(".svg") and s.lower() in text.lower():
            raise SystemExit(f"REFUSED: {where} contains copy-deck string '{s}' ({sid}); exact text is composed by code, never generated")


def build(form3: dict) -> dict:
    board = form3["board"]
    deck = form3.get("copy_deck", {}).get("strings", {})
    style = board.get("style_line") or DEFAULT_STYLE
    negative = board.get("negative_line") or DEFAULT_NEGATIVE
    audio = board.get("audio", {})
    audio_line = None
    if board.get("kind") == "film":
        parts = []
        if audio.get("native_audio"):
            parts.append("Native ambient sound only")
        if (audio.get("voice_over") or "none").lower() == "none":
            parts.append("no speech, no singing, no music")
        audio_line = (", ".join(parts) + ".") if parts else None
    prompts = {}
    for beat in board["beats"]:
        n = beat["n"]
        if beat.get("clip_s", 0) == 0 and board.get("kind") == "film" and "code" in beat.get("title", "").lower():
            continue  # a code-composed beat (end card) has no generated media
        framing, feeling, impact = beat["framing"].strip(), beat["feeling"].strip(), beat["impact"].strip()
        _guard_copy(framing + " " + feeling + " " + impact, deck, f"beat {n}")
        first = (beat.get("first_frame") or "").strip()
        if board.get("kind") == "film" and not first:
            raise SystemExit(f"REFUSED: beat {n} has no first_frame; a film still must describe the state at t_in (Mokobara D1)")
        still_subject = first or framing
        still = " ".join(filter(None, [
            f"{style}.",
            _sentence(still_subject),
            *_anchor_lines(board, beat),
            f"Direction: {feeling}." if feeling else None,
            negative,
        ]))
        motion = None
        if board.get("kind") == "film":
            motion = " ".join(filter(None, [
                f"Image-to-video, {beat.get('clip_s', 0):g} s, the first frame is the supplied still.",
                _sentence(framing),
                _sentence(impact),
                audio_line,
                negative,
            ]))
        prompts[n] = {"title": beat["title"], "still": still, "motion": motion}
    return prompts


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("job_dir")
    ap.add_argument("--out", default="gen/prompts", help="relative to job_dir")
    ap.add_argument("--print", action="store_true", help="print instead of writing")
    a = ap.parse_args(argv)
    job = Path(a.job_dir)
    form3 = json.loads((job / "stages" / "03-creative.json").read_text(encoding="utf-8"))
    prompts = build(form3)
    if a.print:
        for n, p in prompts.items():
            print(f"--- beat {n}: {p['title']}\n[still] {p['still']}\n[motion] {p['motion']}")
        return 0
    out = job / a.out
    out.mkdir(parents=True, exist_ok=True)
    for n, p in prompts.items():
        (out / f"b{n}-still.txt").write_text(p["still"] + "\n", encoding="utf-8")
        if p["motion"]:
            (out / f"b{n}-clip.txt").write_text(p["motion"] + "\n", encoding="utf-8")
    (out / "PROMPTS-BUILT-FROM.json").write_text(json.dumps({"form": "stages/03-creative.json", "beats": list(prompts)}, indent=1), encoding="utf-8")
    print(f"wrote {len(prompts)} beats to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
