#!/usr/bin/env python3
"""Compiled-doctrine gate CLI (CANON-GATE-001 plan §B run_gate.py). Exit 0 on PASS, 1 otherwise.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Run from the repo root, like canon/validation/validate_*.py:

  python3 canon/gate/run_gate.py pre --package P.txt [--prompt-file F ...]
      [--dispatch request.json] --modality {static_image,video,image_sequence,audio}
      [--product] [--packs a,b] [--validate-packs] [--json PATH]
  python3 canon/gate/run_gate.py post --artifact A --dispatch request.json [--package P.txt]
      [--frames DIR] [--detector none|scripted:FILE.json] [--record record.json]
      --modality ... [--product] [--json PATH]

The dispatch descriptor is the committed `*.request.json` shape (parameters.aspectRatio /
durationSeconds / resolution for video; generationConfig.imageConfig.aspectRatio for image).
`--detector` offers no paid option: invoking Cloud Vision is a separate Controller spend
authorisation, not a flag. `--validate-packs` runs the full compiled-pack validator (~15 s)
before the gate; the cheap fail-closed HOLD scan at registry load always runs.

A gate PASS establishes structure over the submitted bytes — not doctrine satisfaction,
quality, outcomes, or adoption.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from canon.gate import doctrine, postdraw, predispatch, textscan  # noqa: E402

MODALITIES = ("static_image", "video", "image_sequence", "audio")
FRAME_SUFFIXES = {".jpg", ".jpeg", ".png"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="run_gate.py", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="gate", required=True)

    def common(p):
        p.add_argument("--modality", required=True, choices=MODALITIES)
        p.add_argument("--product", action="store_true",
                       help="a product/packshot entity is present (selects product_appearance)")
        p.add_argument("--packs", help="comma-separated compiled pack ids; overrides selection")
        p.add_argument("--json", metavar="PATH", help="write the report as JSON")
        p.add_argument("--validate-packs", action="store_true",
                       help="run canon/validation/validate_compiled_pack.py first (~15 s)")

    pre = sub.add_parser("pre", help="pre-dispatch gate over a FINAL_PRODUCTION_PACKAGE")
    pre.add_argument("--package", required=True)
    pre.add_argument("--prompt-file", action="append", default=[],
                     help="use this prompt text instead of extracting from the package")
    pre.add_argument("--dispatch", help="request.json to compare the declared aspect against")
    common(pre)

    post = sub.add_parser("post", help="post-draw gate over an artifact")
    post.add_argument("--artifact", required=True)
    post.add_argument("--dispatch", required=True, help="the committed request.json")
    post.add_argument("--package", help="the package, for the declared minimum dimensions")
    post.add_argument("--frames", metavar="DIR", help="JPEG/PNG frames of a video to scan")
    post.add_argument("--detector", default="none",
                      help="none (default) | scripted:FILE.json (sha256 -> {status, transcript})")
    post.add_argument("--record", help="the artifact's record.json (sha256 cross-check)")
    common(post)
    return parser


def load_detector(spec: str, parser):
    if spec == "none":
        return textscan.NoDetector()
    if spec.startswith("scripted:"):
        doc = json.loads(pathlib.Path(spec[len("scripted:"):]).read_text(encoding="utf-8"))
        return textscan.ScriptedDetector.from_json(doc)
    parser.error(f"--detector {spec!r}: only 'none' or 'scripted:FILE.json' exist; a paid "
                 "detector needs a separate spend authorisation, not a flag")


def load_frames(directory):
    if not directory:
        return None
    files = sorted(p for p in pathlib.Path(directory).iterdir()
                   if p.suffix.lower() in FRAME_SUFFIXES)
    return [p.read_bytes() for p in files]


def validate_packs() -> int:
    """The full compiled-pack validator, as its own main runs it (packs, trigger table,
    reproducibility, HOLD scan); its PASS/FAIL lines print first, the gate follows."""
    from canon.validation import validate_compiled_pack as vcp
    if vcp.main([]):
        print("FAIL pack validation — the gate does not run over unvalidated packs")
        return 1
    print("PASS pack validation (validate_compiled_pack.main: both packs, trigger table, "
          "reproducibility, HOLD-id scan)")
    return 0


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.validate_packs and validate_packs():
        return 1
    try:
        registry = doctrine.load_registry()
    except doctrine.RegistryError as exc:
        print(f"FAIL registry: {exc}")
        return 1
    packs = None
    if args.packs:
        packs = [p.strip() for p in args.packs.split(",") if p.strip()]
        unknown = [p for p in packs if p not in registry.packs]
        if unknown:
            parser.error(f"--packs: {unknown} not among the compiled packs "
                         f"{sorted(registry.packs)}")

    if args.gate == "pre":
        package_path = pathlib.Path(args.package)
        prompts = None
        if args.prompt_file:
            prompts = [pathlib.Path(f).read_text(encoding="utf-8") for f in args.prompt_file]
        dispatch = None
        if args.dispatch:
            dispatch = json.loads(pathlib.Path(args.dispatch).read_text(encoding="utf-8"))
        report = predispatch.run_predispatch(
            package_path.read_text(encoding="utf-8"), prompts, dispatch, args.modality,
            args.product, registry, label=package_path.name, packs=packs)
    else:
        artifact_path = pathlib.Path(args.artifact)
        dispatch = json.loads(pathlib.Path(args.dispatch).read_text(encoding="utf-8"))
        package_text = (pathlib.Path(args.package).read_text(encoding="utf-8")
                        if args.package else None)
        record = (json.loads(pathlib.Path(args.record).read_text(encoding="utf-8"))
                  if args.record else None)
        report = postdraw.run_postdraw(
            artifact_path.read_bytes(), dispatch, package_text,
            load_detector(args.detector, parser), load_frames(args.frames), args.modality,
            args.product, registry, label=artifact_path.name, record=record, packs=packs)

    print(report.render_text())
    if args.json:
        pathlib.Path(args.json).write_text(
            json.dumps(report.to_json(), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if report.verdict() == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
